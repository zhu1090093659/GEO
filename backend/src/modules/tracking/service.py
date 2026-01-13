"""
Tracking Module - Business Logic Service

Handles conversation storage, brand mention extraction,
and visibility score calculation using SQLite database.
"""
from datetime import datetime, timedelta
from typing import List, Optional
import uuid
import re

from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import (
    Conversation, Message, BrandMention, VisibilityScore, Brand,
    Platform, MessageRole, MentionType
)
from .schemas import (
    ConversationUploadItem,
    MessageUploadItem,
    UploadResponse,
    VisibilityResponse,
    VisibilityTrendItem,
    RankingResponse,
    RankingItem,
    StatsResponse,
)


def normalize_brand_name(name: str) -> str:
    """Normalize brand name for consistent matching."""
    return re.sub(r'[^a-z0-9]', '', name.lower())


class TrackingService:
    """Service for tracking brand visibility in AI responses."""

    async def upload_conversations(
        self,
        db: AsyncSession,
        items: List[ConversationUploadItem]
    ) -> UploadResponse:
        """
        Process uploaded conversation data from extension.
        
        Args:
            db: Database session
            items: List of conversation items from browser extension
            
        Returns:
            Upload result with counts
        """
        processed = 0
        brand_mentions_found = 0
        errors = []

        for item in items:
            try:
                # Parse timestamp
                captured_at = datetime.fromisoformat(
                    item.captured_at.replace('Z', '+00:00')
                )
                
                # Get first user message as initial query
                initial_query = ""
                for msg in item.messages:
                    if msg.role == "user":
                        initial_query = msg.content[:500]  # Truncate for storage
                        break
                
                # Validate platform
                try:
                    platform = Platform(item.platform.lower())
                except ValueError:
                    platform = Platform.OTHER
                
                # Create conversation
                conversation = Conversation(
                    id=item.id,
                    session_id=item.session_id,
                    platform=platform,
                    initial_query=initial_query,
                    captured_at=captured_at,
                    language=item.metadata.get('language') if item.metadata else None,
                    region=item.metadata.get('region') if item.metadata else None,
                    user_agent=item.metadata.get('userAgent') if item.metadata else None,
                )
                db.add(conversation)
                
                # Create messages
                for seq, msg_item in enumerate(item.messages):
                    try:
                        role = MessageRole(msg_item.role.lower())
                    except ValueError:
                        role = MessageRole.USER
                    
                    msg_timestamp = captured_at
                    if msg_item.timestamp:
                        try:
                            msg_timestamp = datetime.fromisoformat(
                                msg_item.timestamp.replace('Z', '+00:00')
                            )
                        except ValueError:
                            pass
                    
                    message = Message(
                        conversation_id=item.id,
                        role=role,
                        content=msg_item.content,
                        sequence=seq,
                        timestamp=msg_timestamp,
                    )
                    db.add(message)
                
                # Flush to get message IDs
                await db.flush()
                
                # Extract brand mentions from assistant messages
                mentions = await self._extract_mentions(db, conversation, item.messages)
                brand_mentions_found += len(mentions)
                
                processed += 1
                
            except Exception as e:
                errors.append(f"Error processing {item.id}: {str(e)}")
                await db.rollback()

        # Commit all changes
        await db.commit()

        return UploadResponse(
            received=len(items),
            processed=processed,
            brand_mentions_found=brand_mentions_found,
            errors=errors,
        )

    async def _extract_mentions(
        self,
        db: AsyncSession,
        conversation: Conversation,
        messages: List[MessageUploadItem]
    ) -> List[BrandMention]:
        """
        Extract brand mentions from conversation.
        
        Currently uses simple keyword matching against registered brands.
        TODO: Implement Claude API for advanced NER.
        
        Args:
            db: Database session
            conversation: Parent conversation
            messages: List of messages to analyze
            
        Returns:
            List of created brand mentions
        """
        mentions = []
        
        # Get registered brands
        result = await db.execute(
            select(Brand).where(Brand.is_active == True)
        )
        brands = result.scalars().all()
        
        if not brands:
            return mentions
        
        # Get message records for this conversation
        msg_result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .where(Message.role == MessageRole.ASSISTANT)
            .order_by(Message.sequence)
        )
        db_messages = msg_result.scalars().all()
        
        # Search for brand mentions in assistant messages
        for db_msg in db_messages:
            content_lower = db_msg.content.lower()
            
            for brand in brands:
                # Check brand name and aliases
                names_to_check = [brand.name]
                if brand.aliases:
                    try:
                        import json
                        aliases = json.loads(brand.aliases)
                        names_to_check.extend(aliases)
                    except (json.JSONDecodeError, TypeError):
                        pass
                
                for name in names_to_check:
                    name_lower = name.lower()
                    pos = content_lower.find(name_lower)
                    
                    if pos >= 0:
                        # Extract context (±100 chars)
                        start = max(0, pos - 100)
                        end = min(len(db_msg.content), pos + len(name) + 100)
                        context = db_msg.content[start:end]
                        
                        # Determine mention type (simple heuristic)
                        mention_type = self._classify_mention(
                            db_msg.content, pos, name
                        )
                        
                        mention = BrandMention(
                            conversation_id=conversation.id,
                            message_id=db_msg.id,
                            brand_name=brand.name,
                            brand_normalized=brand.normalized_name,
                            mention_type=mention_type,
                            position=pos,
                            context=context,
                            sentiment=0.0,  # TODO: Implement sentiment analysis
                            confidence=0.8,
                        )
                        db.add(mention)
                        mentions.append(mention)
                        break  # Only count first occurrence per brand per message
        
        return mentions

    def _classify_mention(
        self, content: str, position: int, brand_name: str
    ) -> MentionType:
        """
        Classify the type of brand mention based on context.
        
        Simple heuristic implementation.
        TODO: Use Claude API for better classification.
        """
        # Get surrounding context
        start = max(0, position - 50)
        end = min(len(content), position + len(brand_name) + 50)
        context = content[start:end].lower()
        
        # Check for recommendation patterns
        recommend_patterns = [
            'recommend', 'suggest', 'try', 'consider', 'best',
            'top pick', 'great choice', 'highly rated'
        ]
        if any(p in context for p in recommend_patterns):
            return MentionType.RECOMMENDATION
        
        # Check for comparison patterns
        compare_patterns = [
            'compared to', 'versus', 'vs', 'better than', 'worse than',
            'similar to', 'alternative to', 'like'
        ]
        if any(p in context for p in compare_patterns):
            return MentionType.COMPARISON
        
        # Check for negative patterns
        negative_patterns = [
            'not recommend', 'avoid', 'issue', 'problem', 'bad',
            'poor', 'disappointing', 'don\'t'
        ]
        if any(p in context for p in negative_patterns):
            return MentionType.NEGATIVE
        
        return MentionType.DIRECT

    async def get_visibility(
        self,
        db: AsyncSession,
        brand: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        platform: Optional[str] = None,
    ) -> VisibilityResponse:
        """
        Get visibility data for a brand.
        
        Args:
            db: Database session
            brand: Brand name to query
            start_date: Optional start date filter
            end_date: Optional end date filter
            platform: Optional platform filter
            
        Returns:
            Visibility data including score and trend
        """
        # Default date range: last 30 days
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        period_days = (end_date - start_date).days
        brand_normalized = normalize_brand_name(brand)
        
        # Query visibility scores
        query = (
            select(VisibilityScore)
            .where(VisibilityScore.brand_normalized == brand_normalized)
            .where(VisibilityScore.date >= start_date)
            .where(VisibilityScore.date <= end_date)
            .order_by(VisibilityScore.date)
        )
        
        if platform:
            try:
                plat = Platform(platform.lower())
                query = query.where(VisibilityScore.platform == plat)
            except ValueError:
                pass
        
        result = await db.execute(query)
        scores = result.scalars().all()
        
        # Calculate metrics
        if scores:
            current_score = scores[-1].score
            previous_score = scores[0].score if len(scores) > 1 else None
            change_percent = (
                ((current_score - previous_score) / previous_score * 100)
                if previous_score and previous_score > 0
                else None
            )
            total_mentions = sum(s.mention_count for s in scores)
            avg_sentiment = (
                sum(s.avg_sentiment for s in scores) / len(scores)
                if scores else 0.0
            )
        else:
            # No scores yet - calculate from mentions
            mention_result = await db.execute(
                select(func.count(BrandMention.id), func.avg(BrandMention.sentiment))
                .where(BrandMention.brand_normalized == brand_normalized)
                .where(BrandMention.created_at >= start_date)
                .where(BrandMention.created_at <= end_date)
            )
            row = mention_result.one()
            total_mentions = row[0] or 0
            avg_sentiment = row[1] or 0.0
            current_score = min(100, total_mentions * 5)  # Simple score
            previous_score = None
            change_percent = None
        
        # Build trend data
        trend = [
            VisibilityTrendItem(
                date=s.date.strftime('%Y-%m-%d'),
                score=s.score,
                mention_count=s.mention_count,
                sentiment=s.avg_sentiment,
            )
            for s in scores
        ]

        return VisibilityResponse(
            brand=brand,
            current_score=current_score,
            previous_score=previous_score,
            change_percent=change_percent,
            trend=trend,
            total_mentions=total_mentions,
            avg_sentiment=avg_sentiment,
            period_days=period_days,
        )

    async def get_ranking(
        self,
        db: AsyncSession,
        brand: str,
        competitors: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 10,
    ) -> RankingResponse:
        """
        Get ranking data for a brand compared to competitors.
        
        Args:
            db: Database session
            brand: Brand name to query
            competitors: Optional list of competitor names
            start_date: Optional start date filter
            end_date: Optional end date filter
            limit: Maximum number of results
            
        Returns:
            Ranking data with competitor comparison
        """
        # Default date range
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        brand_normalized = normalize_brand_name(brand)
        
        # Get brands to compare
        if competitors:
            competitor_normalized = [normalize_brand_name(c) for c in competitors]
            all_brands = [brand_normalized] + competitor_normalized
        else:
            # Get top brands by mention count
            top_result = await db.execute(
                select(BrandMention.brand_normalized, func.count(BrandMention.id).label('cnt'))
                .where(BrandMention.created_at >= start_date)
                .where(BrandMention.created_at <= end_date)
                .group_by(BrandMention.brand_normalized)
                .order_by(desc('cnt'))
                .limit(limit + 1)
            )
            all_brands = [row[0] for row in top_result.all()]
            if brand_normalized not in all_brands:
                all_brands.append(brand_normalized)
        
        # Calculate scores for each brand
        rankings = []
        for bn in all_brands:
            # Get latest visibility score
            score_result = await db.execute(
                select(VisibilityScore)
                .where(VisibilityScore.brand_normalized == bn)
                .where(VisibilityScore.date >= start_date)
                .order_by(desc(VisibilityScore.date))
                .limit(1)
            )
            latest_score = score_result.scalar_one_or_none()
            
            # Get mention count
            mention_result = await db.execute(
                select(func.count(BrandMention.id))
                .where(BrandMention.brand_normalized == bn)
                .where(BrandMention.created_at >= start_date)
                .where(BrandMention.created_at <= end_date)
            )
            mention_count = mention_result.scalar() or 0
            
            # Get brand display name
            brand_result = await db.execute(
                select(Brand.name).where(Brand.normalized_name == bn)
            )
            display_name = brand_result.scalar() or bn
            
            score = latest_score.score if latest_score else min(100, mention_count * 5)
            
            rankings.append(RankingItem(
                brand_name=display_name,
                score=score,
                rank=0,  # Will be set after sorting
                mention_count=mention_count,
                trend="stable",  # TODO: Calculate trend
                change=None,
            ))
        
        # Sort by score descending and assign ranks
        rankings.sort(key=lambda x: x.score, reverse=True)
        for i, r in enumerate(rankings):
            r.rank = i + 1
        
        # Find target brand
        brand_item = next(
            (r for r in rankings if normalize_brand_name(r.brand_name) == brand_normalized),
            None
        )
        brand_rank = brand_item.rank if brand_item else 0
        brand_score = brand_item.score if brand_item else 0.0
        
        # Filter out target brand from competitors list
        competitor_rankings = [
            r for r in rankings
            if normalize_brand_name(r.brand_name) != brand_normalized
        ][:limit]

        return RankingResponse(
            brand=brand,
            brand_rank=brand_rank,
            brand_score=brand_score,
            rankings=competitor_rankings,
            total_brands=len(rankings),
            period=f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        )

    async def get_stats(self, db: AsyncSession) -> StatsResponse:
        """Get overall tracking statistics."""
        # Count conversations
        conv_result = await db.execute(select(func.count(Conversation.id)))
        total_conversations = conv_result.scalar() or 0
        
        # Count messages
        msg_result = await db.execute(select(func.count(Message.id)))
        total_messages = msg_result.scalar() or 0
        
        # Count brand mentions
        mention_result = await db.execute(select(func.count(BrandMention.id)))
        total_mentions = mention_result.scalar() or 0
        
        # Count tracked brands
        brand_result = await db.execute(
            select(func.count(Brand.id)).where(Brand.is_active == True)
        )
        total_brands = brand_result.scalar() or 0
        
        # Platform breakdown
        platform_result = await db.execute(
            select(Conversation.platform, func.count(Conversation.id))
            .group_by(Conversation.platform)
        )
        platforms = {str(row[0].value): row[1] for row in platform_result.all()}
        
        # Date range
        date_result = await db.execute(
            select(
                func.min(Conversation.captured_at),
                func.max(Conversation.captured_at)
            )
        )
        date_row = date_result.one()
        date_range = {
            "earliest": date_row[0].isoformat() if date_row[0] else None,
            "latest": date_row[1].isoformat() if date_row[1] else None,
        }
        
        return StatsResponse(
            total_conversations=total_conversations,
            total_messages=total_messages,
            total_brand_mentions=total_mentions,
            total_brands_tracked=total_brands,
            platforms=platforms,
            date_range=date_range,
        )

    async def register_brand(
        self,
        db: AsyncSession,
        name: str,
        category: Optional[str] = None,
        description: Optional[str] = None,
        website: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        is_competitor: bool = False,
    ) -> Brand:
        """
        Register a brand for tracking.
        
        Args:
            db: Database session
            name: Brand name
            category: Optional category
            description: Optional description
            website: Optional website URL
            aliases: Optional list of aliases
            is_competitor: Whether this is a competitor brand
            
        Returns:
            Created brand record
        """
        import json
        
        normalized = normalize_brand_name(name)
        
        brand = Brand(
            name=name,
            normalized_name=normalized,
            category=category,
            description=description,
            website=website,
            aliases=json.dumps(aliases) if aliases else None,
            is_competitor=is_competitor,
        )
        db.add(brand)
        await db.commit()
        await db.refresh(brand)
        
        return brand


# Global service instance
tracking_service = TrackingService()
