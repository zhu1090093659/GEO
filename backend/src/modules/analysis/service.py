"""
Analysis Module - Business Logic Service

Handles competitor analysis, sentiment analysis,
and topic discovery using database storage.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json
import re

from sqlalchemy import select, func, and_, desc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import (
    CompetitorGroup, ComparisonResult, SentimentAnalysis,
    Topic, Keyword, competitor_group_brands
)
from .schemas import (
    CompetitorComparisonResponse,
    CompetitorItem,
    CompetitorGroupResponse,
    ComparisonDetailResponse,
    SentimentResponse,
    SentimentDistribution,
    SentimentSample,
    SentimentTrendItem,
    TopicDiscoveryResponse,
    TopicItem,
    KeywordItem,
    AnalysisStatsResponse,
)

# Import tracking models for data access
from src.modules.tracking.models import Brand, BrandMention, VisibilityScore, Conversation


def normalize_name(name: str) -> str:
    """Normalize a name for consistent matching."""
    return re.sub(r'[^a-z0-9]', '', name.lower())


class AnalysisService:
    """Service for competitor, sentiment, and topic analysis."""
    
    # ========================================
    # Competitor Group Management
    # ========================================
    
    async def create_competitor_group(
        self,
        db: AsyncSession,
        name: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        owner_brand: Optional[str] = None,
        competitor_names: Optional[List[str]] = None,
    ) -> CompetitorGroup:
        """
        Create a new competitor group.
        
        Args:
            db: Database session
            name: Group name
            description: Group description
            category: Industry category
            owner_brand: Name of the owner brand
            competitor_names: List of competitor brand names
            
        Returns:
            Created competitor group
        """
        # Find owner brand if specified
        owner_brand_id = None
        if owner_brand:
            result = await db.execute(
                select(Brand).where(Brand.normalized_name == normalize_name(owner_brand))
            )
            brand = result.scalar_one_or_none()
            if brand:
                owner_brand_id = brand.id
        
        # Create group
        group = CompetitorGroup(
            name=name,
            description=description,
            category=category,
            owner_brand_id=owner_brand_id,
        )
        db.add(group)
        await db.flush()
        
        # Add competitors via association table directly
        if competitor_names:
            for comp_name in competitor_names:
                # Find or create brand
                brand = await self._get_or_create_brand(db, comp_name, is_competitor=True)
                # Insert into association table directly
                await db.execute(
                    competitor_group_brands.insert().values(
                        group_id=group.id,
                        brand_id=brand.id
                    )
                )
        
        await db.commit()
        
        # Reload with brands relationship
        result = await db.execute(
            select(CompetitorGroup)
            .where(CompetitorGroup.id == group.id)
            .options(selectinload(CompetitorGroup.brands))
        )
        return result.scalar_one()
    
    async def _get_or_create_brand(
        self, db: AsyncSession, name: str, is_competitor: bool = False
    ) -> Brand:
        """Get existing brand or create new one."""
        normalized = normalize_name(name)
        result = await db.execute(
            select(Brand).where(Brand.normalized_name == normalized)
        )
        brand = result.scalar_one_or_none()
        
        if not brand:
            brand = Brand(
                name=name,
                normalized_name=normalized,
                is_competitor=is_competitor,
            )
            db.add(brand)
            await db.flush()
        
        return brand
    
    async def get_competitor_groups(
        self, db: AsyncSession, category: Optional[str] = None
    ) -> List[CompetitorGroup]:
        """Get all competitor groups, optionally filtered by category."""
        query = (
            select(CompetitorGroup)
            .where(CompetitorGroup.is_active == True)
            .options(selectinload(CompetitorGroup.brands))
        )
        
        if category:
            query = query.where(CompetitorGroup.category == category)
        
        result = await db.execute(query.order_by(CompetitorGroup.name))
        return list(result.scalars().all())
    
    async def get_competitor_group(
        self, db: AsyncSession, group_id: int
    ) -> Optional[CompetitorGroup]:
        """Get a specific competitor group by ID."""
        result = await db.execute(
            select(CompetitorGroup)
            .where(CompetitorGroup.id == group_id)
            .options(selectinload(CompetitorGroup.brands))
        )
        return result.scalar_one_or_none()
    
    async def add_competitor_to_group(
        self, db: AsyncSession, group_id: int, competitor_name: str
    ) -> bool:
        """Add a competitor to an existing group."""
        group = await self.get_competitor_group(db, group_id)
        if not group:
            return False
        
        brand = await self._get_or_create_brand(db, competitor_name, is_competitor=True)
        
        # Check if already in group
        existing_brand_ids = [b.id for b in group.brands]
        if brand.id not in existing_brand_ids:
            await db.execute(
                competitor_group_brands.insert().values(
                    group_id=group.id,
                    brand_id=brand.id
                )
            )
            await db.commit()
        
        return True
    
    async def remove_competitor_from_group(
        self, db: AsyncSession, group_id: int, competitor_name: str
    ) -> bool:
        """Remove a competitor from a group."""
        group = await self.get_competitor_group(db, group_id)
        if not group:
            return False
        
        normalized = normalize_name(competitor_name)
        for brand in group.brands:
            if brand.normalized_name == normalized:
                # Delete from association table
                await db.execute(
                    competitor_group_brands.delete().where(
                        and_(
                            competitor_group_brands.c.group_id == group.id,
                            competitor_group_brands.c.brand_id == brand.id
                        )
                    )
                )
                await db.commit()
                return True
        
        return False
    
    async def delete_competitor_group(
        self, db: AsyncSession, group_id: int
    ) -> bool:
        """Delete a competitor group."""
        group = await self.get_competitor_group(db, group_id)
        if not group:
            return False
        
        await db.delete(group)
        await db.commit()
        return True
    
    # ========================================
    # Competitor Comparison
    # ========================================
    
    async def compare_competitors(
        self,
        db: AsyncSession,
        brand: str,
        competitors: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> CompetitorComparisonResponse:
        """
        Compare brand visibility against competitors.
        
        Args:
            db: Database session
            brand: Target brand name
            competitors: List of competitor names (or use all tracked)
            start_date: Start of analysis period
            end_date: End of analysis period
            
        Returns:
            Comparison data with rankings
        """
        # Default date range
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        brand_normalized = normalize_name(brand)
        
        # Get competitors list
        if not competitors:
            # Get all tracked competitor brands
            result = await db.execute(
                select(Brand).where(Brand.is_competitor == True).where(Brand.is_active == True)
            )
            competitors = [b.name for b in result.scalars().all()]
        
        # Get brand metrics
        brand_metrics = await self._get_brand_metrics(
            db, brand_normalized, start_date, end_date
        )
        
        # Get competitor metrics
        comparison_items = []
        for comp_name in competitors:
            comp_normalized = normalize_name(comp_name)
            if comp_normalized == brand_normalized:
                continue
            
            metrics = await self._get_brand_metrics(
                db, comp_normalized, start_date, end_date
            )
            
            comparison_items.append(CompetitorItem(
                name=comp_name,
                visibility_score=metrics.get('visibility_score', 0),
                mention_count=metrics.get('mention_count', 0),
                rank=0,  # Will be set after sorting
                sentiment=metrics.get('avg_sentiment', 0),
                trend=metrics.get('trend', 'stable'),
            ))
        
        # Add brand to list for ranking
        all_items = [
            CompetitorItem(
                name=brand,
                visibility_score=brand_metrics.get('visibility_score', 0),
                mention_count=brand_metrics.get('mention_count', 0),
                rank=0,
                sentiment=brand_metrics.get('avg_sentiment', 0),
                trend=brand_metrics.get('trend', 'stable'),
            )
        ] + comparison_items
        
        # Sort by score and assign ranks
        all_items.sort(key=lambda x: x.visibility_score, reverse=True)
        for i, item in enumerate(all_items):
            item.rank = i + 1
        
        # Find brand rank
        brand_item = next((x for x in all_items if normalize_name(x.name) == brand_normalized), None)
        
        return CompetitorComparisonResponse(
            brand=brand,
            brand_score=brand_item.visibility_score if brand_item else 0,
            brand_rank=brand_item.rank if brand_item else 0,
            brand_mentions=brand_metrics.get('mention_count', 0),
            brand_sentiment=brand_metrics.get('avg_sentiment', 0),
            competitors=[x for x in all_items if normalize_name(x.name) != brand_normalized],
            insights=None,  # TODO: Generate with Claude
            analysis_date=datetime.utcnow(),
            period=f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        )
    
    async def _get_brand_metrics(
        self,
        db: AsyncSession,
        brand_normalized: str,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Any]:
        """Get visibility and sentiment metrics for a brand."""
        # Get latest visibility score
        score_result = await db.execute(
            select(VisibilityScore)
            .where(VisibilityScore.brand_normalized == brand_normalized)
            .where(VisibilityScore.date >= start_date)
            .where(VisibilityScore.date <= end_date)
            .order_by(desc(VisibilityScore.date))
            .limit(1)
        )
        latest_score = score_result.scalar_one_or_none()
        
        # Get mention count and sentiment
        mention_result = await db.execute(
            select(
                func.count(BrandMention.id),
                func.avg(BrandMention.sentiment)
            )
            .where(BrandMention.brand_normalized == brand_normalized)
            .where(BrandMention.created_at >= start_date)
            .where(BrandMention.created_at <= end_date)
        )
        row = mention_result.one()
        mention_count = row[0] or 0
        avg_sentiment = row[1] or 0.0
        
        return {
            'visibility_score': latest_score.score if latest_score else min(100, mention_count * 5),
            'mention_count': mention_count,
            'avg_sentiment': round(avg_sentiment, 2),
            'trend': 'stable',  # TODO: Calculate trend
        }
    
    # ========================================
    # Sentiment Analysis
    # ========================================
    
    async def analyze_sentiment(
        self,
        db: AsyncSession,
        brand: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> SentimentResponse:
        """
        Analyze sentiment for a brand in AI responses.
        
        Args:
            db: Database session
            brand: Brand name to analyze
            start_date: Start of analysis period
            end_date: End of analysis period
            
        Returns:
            Sentiment analysis results
        """
        # Default date range
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=30)
        
        period_days = (end_date - start_date).days
        brand_normalized = normalize_name(brand)
        
        # Get all mentions with sentiment
        result = await db.execute(
            select(BrandMention)
            .where(BrandMention.brand_normalized == brand_normalized)
            .where(BrandMention.created_at >= start_date)
            .where(BrandMention.created_at <= end_date)
            .order_by(desc(BrandMention.created_at))
        )
        mentions = result.scalars().all()
        
        if not mentions:
            return SentimentResponse(
                brand=brand,
                overall_sentiment=0.0,
                sentiment_label="neutral",
                distribution=SentimentDistribution(positive=0, neutral=100, negative=0),
                trend=[],
                samples=[],
                mentions_analyzed=0,
                period_days=period_days,
            )
        
        # Calculate sentiment distribution
        sentiments = [m.sentiment for m in mentions]
        overall = sum(sentiments) / len(sentiments)
        
        positive_count = sum(1 for s in sentiments if s > 0.3)
        negative_count = sum(1 for s in sentiments if s < -0.3)
        neutral_count = len(sentiments) - positive_count - negative_count
        
        total = len(sentiments)
        distribution = SentimentDistribution(
            positive=round(positive_count / total * 100, 1),
            neutral=round(neutral_count / total * 100, 1),
            negative=round(negative_count / total * 100, 1),
        )
        
        # Determine label
        if overall > 0.3:
            label = "positive"
        elif overall < -0.3:
            label = "negative"
        else:
            label = "neutral"
        
        # Build trend (daily aggregation)
        trend = await self._build_sentiment_trend(
            db, brand_normalized, start_date, end_date
        )
        
        # Get sample responses
        samples = await self._get_sentiment_samples(db, mentions[:10])
        
        return SentimentResponse(
            brand=brand,
            overall_sentiment=round(overall, 2),
            sentiment_label=label,
            distribution=distribution,
            trend=trend,
            samples=samples,
            mentions_analyzed=len(mentions),
            period_days=period_days,
        )
    
    async def _build_sentiment_trend(
        self,
        db: AsyncSession,
        brand_normalized: str,
        start_date: datetime,
        end_date: datetime,
    ) -> List[SentimentTrendItem]:
        """Build daily sentiment trend."""
        result = await db.execute(
            select(
                func.date(BrandMention.created_at).label('date'),
                func.avg(BrandMention.sentiment).label('avg_sentiment'),
                func.count(BrandMention.id).label('count')
            )
            .where(BrandMention.brand_normalized == brand_normalized)
            .where(BrandMention.created_at >= start_date)
            .where(BrandMention.created_at <= end_date)
            .group_by(func.date(BrandMention.created_at))
            .order_by(func.date(BrandMention.created_at))
        )
        
        return [
            SentimentTrendItem(
                date=str(row.date),
                sentiment=round(row.avg_sentiment, 2),
                mention_count=row.count,
            )
            for row in result.all()
        ]
    
    async def _get_sentiment_samples(
        self, db: AsyncSession, mentions: List[BrandMention]
    ) -> List[SentimentSample]:
        """Get sample responses for sentiment display."""
        samples = []
        
        for mention in mentions[:5]:
            # Get conversation for this mention
            conv_result = await db.execute(
                select(Conversation).where(Conversation.id == mention.conversation_id)
            )
            conv = conv_result.scalar_one_or_none()
            
            if conv:
                label = "positive" if mention.sentiment > 0.3 else ("negative" if mention.sentiment < -0.3 else "neutral")
                samples.append(SentimentSample(
                    query=conv.initial_query[:200] if conv.initial_query else "",
                    response_snippet=mention.context[:200] if mention.context else "",
                    sentiment_score=mention.sentiment,
                    sentiment_label=label,
                    platform=conv.platform.value if conv.platform else None,
                    timestamp=mention.created_at,
                ))
        
        return samples
    
    # ========================================
    # Topic Discovery & Keyword Extraction
    # ========================================
    
    async def extract_topics_from_conversations(
        self,
        db: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Extract topics and keywords from recent conversations.
        
        This is a simplified extraction that can be enhanced with Claude API
        for more sophisticated topic modeling.
        
        Args:
            db: Database session
            start_date: Start of analysis period
            end_date: End of analysis period
            
        Returns:
            Extraction results with topics and keywords created/updated
        """
        if not end_date:
            end_date = datetime.utcnow()
        if not start_date:
            start_date = end_date - timedelta(days=7)
        
        # Get all conversations in the period
        result = await db.execute(
            select(Conversation)
            .where(Conversation.captured_at >= start_date)
            .where(Conversation.captured_at <= end_date)
        )
        conversations = result.scalars().all()
        
        if not conversations:
            return {"topics_created": 0, "keywords_created": 0, "conversations_analyzed": 0}
        
        # Extract keywords from queries
        keyword_counts: Dict[str, int] = {}
        brand_associations: Dict[str, set] = {}
        
        for conv in conversations:
            query = conv.initial_query.lower()
            
            # Simple keyword extraction (split by non-alphanumeric)
            words = re.findall(r'\b[a-z]{3,}\b', query)
            
            # Filter common stop words
            stop_words = {
                'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
                'had', 'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been',
                'were', 'this', 'that', 'with', 'what', 'when', 'where', 'which',
                'who', 'will', 'how', 'why', 'from', 'they', 'your', 'more',
                'some', 'than', 'into', 'other', 'about', 'would', 'there',
            }
            
            words = [w for w in words if w not in stop_words]
            
            for word in words:
                keyword_counts[word] = keyword_counts.get(word, 0) + 1
        
        # Create/update keywords in database
        keywords_created = 0
        for word, count in keyword_counts.items():
            if count < 2:  # Skip very rare keywords
                continue
            
            normalized = normalize_name(word)
            
            # Check if keyword exists
            existing = await db.execute(
                select(Keyword).where(Keyword.normalized_word == normalized)
            )
            keyword_obj = existing.scalar_one_or_none()
            
            if keyword_obj:
                keyword_obj.count += count
                keyword_obj.query_count += 1
                keyword_obj.last_seen = datetime.utcnow()
            else:
                keyword_obj = Keyword(
                    word=word,
                    normalized_word=normalized,
                    count=count,
                    query_count=1,
                    trend="stable",
                )
                db.add(keyword_obj)
                keywords_created += 1
        
        # Create simple topic clusters based on common query patterns
        topic_patterns = [
            ("Product Comparison", ["best", "vs", "compare", "comparison", "versus", "alternative"]),
            ("Pricing & Cost", ["price", "cost", "pricing", "free", "cheap", "expensive", "subscription"]),
            ("How-To & Tutorials", ["how", "tutorial", "guide", "learn", "setup", "configure"]),
            ("Reviews & Ratings", ["review", "rating", "worth", "good", "bad", "pros", "cons"]),
            ("Features & Capabilities", ["feature", "capability", "can", "does", "support", "integration"]),
        ]
        
        topics_created = 0
        for topic_name, keywords in topic_patterns:
            # Count queries matching this pattern
            matching_count = sum(
                1 for conv in conversations
                if any(kw in conv.initial_query.lower() for kw in keywords)
            )
            
            if matching_count > 0:
                normalized = normalize_name(topic_name)
                
                # Check if topic exists
                existing = await db.execute(
                    select(Topic).where(Topic.normalized_name == normalized)
                )
                topic_obj = existing.scalar_one_or_none()
                
                if topic_obj:
                    topic_obj.query_count += matching_count
                    topic_obj.last_seen = datetime.utcnow()
                else:
                    topic_obj = Topic(
                        name=topic_name,
                        normalized_name=normalized,
                        query_count=matching_count,
                        keywords=json.dumps(keywords),
                        trend="stable",
                    )
                    db.add(topic_obj)
                    topics_created += 1
        
        await db.commit()
        
        return {
            "topics_created": topics_created,
            "keywords_created": keywords_created,
            "conversations_analyzed": len(conversations),
        }
    
    async def cluster_keywords(
        self,
        db: AsyncSession,
        min_count: int = 5,
    ) -> Dict[str, Any]:
        """
        Cluster keywords into related groups.
        
        Simple clustering based on co-occurrence in queries.
        Can be enhanced with embedding-based clustering using Claude.
        
        Args:
            db: Database session
            min_count: Minimum keyword count to include
            
        Returns:
            Clustering results
        """
        # Get keywords above threshold
        result = await db.execute(
            select(Keyword)
            .where(Keyword.count >= min_count)
            .order_by(desc(Keyword.count))
            .limit(100)
        )
        keywords = result.scalars().all()
        
        if not keywords:
            return {"clusters": [], "keywords_processed": 0}
        
        # Simple clustering: group by related topics
        clusters: Dict[str, List[str]] = {}
        
        for keyword in keywords:
            # Check existing related topics
            related = json.loads(keyword.related_topics) if keyword.related_topics else []
            
            if related:
                for topic in related:
                    if topic not in clusters:
                        clusters[topic] = []
                    clusters[topic].append(keyword.word)
            else:
                # Assign to "General" cluster
                if "General" not in clusters:
                    clusters["General"] = []
                clusters["General"].append(keyword.word)
        
        return {
            "clusters": [
                {"topic": topic, "keywords": kws}
                for topic, kws in clusters.items()
            ],
            "keywords_processed": len(keywords),
        }
    
    async def discover_topics(
        self,
        db: AsyncSession,
        brand: Optional[str] = None,
        limit: int = 20,
    ) -> TopicDiscoveryResponse:
        """
        Discover trending topics and keywords from queries.
        
        Args:
            db: Database session
            brand: Optional brand to filter topics
            limit: Maximum topics to return
            
        Returns:
            Discovered topics and keywords
        """
        # Get topics
        topic_query = (
            select(Topic)
            .where(Topic.is_active == True)
            .order_by(desc(Topic.query_count))
            .limit(limit)
        )
        
        if brand:
            brand_normalized = normalize_name(brand)
            # Filter topics that mention this brand
            topic_query = topic_query.where(
                Topic.related_brands.contains(brand_normalized)
            )
        
        topic_result = await db.execute(topic_query)
        topics = topic_result.scalars().all()
        
        # Get keywords
        keyword_result = await db.execute(
            select(Keyword)
            .order_by(desc(Keyword.count))
            .limit(limit)
        )
        keywords = keyword_result.scalars().all()
        
        # Get total query count
        query_count_result = await db.execute(
            select(func.count(Conversation.id))
        )
        total_queries = query_count_result.scalar() or 0
        
        return TopicDiscoveryResponse(
            topics=[
                TopicItem(
                    id=t.id,
                    name=t.name,
                    query_count=t.query_count,
                    keywords=json.loads(t.keywords) if t.keywords else [],
                    trend=t.trend,
                    growth_rate=t.growth_rate,
                    related_brands=json.loads(t.related_brands) if t.related_brands else [],
                )
                for t in topics
            ],
            keywords=[
                KeywordItem(
                    word=k.word,
                    count=k.count,
                    trend=k.trend,
                    growth_rate=k.growth_rate,
                    related_topics=json.loads(k.related_topics) if k.related_topics else [],
                    related_brands=json.loads(k.related_brands) if k.related_brands else [],
                )
                for k in keywords
            ],
            total_queries_analyzed=total_queries,
            analysis_period="Last 30 days",
        )
    
    # ========================================
    # Statistics
    # ========================================
    
    async def get_stats(self, db: AsyncSession) -> AnalysisStatsResponse:
        """Get overall analysis statistics."""
        # Count competitor groups
        group_result = await db.execute(
            select(func.count(CompetitorGroup.id))
        )
        total_groups = group_result.scalar() or 0
        
        # Count comparisons
        comparison_result = await db.execute(
            select(func.count(ComparisonResult.id))
        )
        total_comparisons = comparison_result.scalar() or 0
        
        # Count sentiment analyses
        sentiment_result = await db.execute(
            select(func.count(SentimentAnalysis.id))
        )
        total_sentiments = sentiment_result.scalar() or 0
        
        # Count topics
        topic_result = await db.execute(
            select(func.count(Topic.id))
        )
        total_topics = topic_result.scalar() or 0
        
        # Count keywords
        keyword_result = await db.execute(
            select(func.count(Keyword.id))
        )
        total_keywords = keyword_result.scalar() or 0
        
        # Get last analysis date
        last_result = await db.execute(
            select(func.max(ComparisonResult.created_at))
        )
        last_analysis = last_result.scalar()
        
        return AnalysisStatsResponse(
            total_competitor_groups=total_groups,
            total_comparisons=total_comparisons,
            total_sentiment_analyses=total_sentiments,
            total_topics=total_topics,
            total_keywords=total_keywords,
            last_analysis_date=last_analysis,
        )


# Global service instance
analysis_service = AnalysisService()
