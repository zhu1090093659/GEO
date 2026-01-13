"""
Tracking Module - Visibility Score Calculator

Calculates visibility scores for brands based on mention frequency,
position, sentiment, and other factors.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import math

from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    Conversation, Message, BrandMention, VisibilityScore, Brand,
    Platform, MentionType
)


class VisibilityCalculator:
    """
    Calculates brand visibility scores.
    
    Score Formula:
    score = (frequency_score * 0.4) + (position_score * 0.3) + (sentiment_score * 0.2) + (type_score * 0.1)
    
    Where:
    - frequency_score: Based on mention count relative to total conversations
    - position_score: Earlier mentions in response score higher
    - sentiment_score: Positive sentiment increases score
    - type_score: Recommendations score higher than comparisons
    """
    
    # Score weights
    WEIGHT_FREQUENCY = 0.4
    WEIGHT_POSITION = 0.3
    WEIGHT_SENTIMENT = 0.2
    WEIGHT_TYPE = 0.1
    
    # Mention type multipliers
    TYPE_MULTIPLIERS = {
        MentionType.RECOMMENDATION: 1.5,
        MentionType.DIRECT: 1.0,
        MentionType.COMPARISON: 0.8,
        MentionType.INDIRECT: 0.6,
        MentionType.NEGATIVE: 0.3,
    }
    
    async def calculate_daily_scores(
        self,
        db: AsyncSession,
        date: Optional[datetime] = None,
        platform: Optional[Platform] = None,
    ) -> List[VisibilityScore]:
        """
        Calculate visibility scores for all brands for a given day.
        
        Args:
            db: Database session
            date: Date to calculate scores for (default: today)
            platform: Optional platform filter
            
        Returns:
            List of created VisibilityScore records
        """
        if date is None:
            date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Get date range for the day
        start_date = date
        end_date = date + timedelta(days=1)
        
        # Get all brands with mentions in this period
        query = (
            select(
                BrandMention.brand_normalized,
                func.count(BrandMention.id).label('mention_count'),
                func.avg(BrandMention.position).label('avg_position'),
                func.avg(BrandMention.sentiment).label('avg_sentiment'),
            )
            .where(BrandMention.created_at >= start_date)
            .where(BrandMention.created_at < end_date)
            .group_by(BrandMention.brand_normalized)
        )
        
        result = await db.execute(query)
        brand_stats = result.all()
        
        if not brand_stats:
            return []
        
        # Get total conversation count for the period
        conv_query = (
            select(func.count(Conversation.id))
            .where(Conversation.captured_at >= start_date)
            .where(Conversation.captured_at < end_date)
        )
        conv_result = await db.execute(conv_query)
        total_conversations = conv_result.scalar() or 1
        
        # Calculate scores for each brand
        scores = []
        for brand_normalized, mention_count, avg_position, avg_sentiment in brand_stats:
            # Get brand display name
            brand_result = await db.execute(
                select(Brand.name).where(Brand.normalized_name == brand_normalized)
            )
            brand_name = brand_result.scalar() or brand_normalized
            
            # Calculate component scores
            frequency_score = self._calculate_frequency_score(
                mention_count, total_conversations
            )
            position_score = self._calculate_position_score(avg_position or 0)
            sentiment_score = self._calculate_sentiment_score(avg_sentiment or 0)
            
            # Get mention type breakdown for type score
            type_score = await self._calculate_type_score(
                db, brand_normalized, start_date, end_date
            )
            
            # Calculate final score
            final_score = (
                frequency_score * self.WEIGHT_FREQUENCY +
                position_score * self.WEIGHT_POSITION +
                sentiment_score * self.WEIGHT_SENTIMENT +
                type_score * self.WEIGHT_TYPE
            )
            
            # Normalize to 0-100 scale
            final_score = min(100, max(0, final_score * 100))
            
            # Create score record
            visibility_score = VisibilityScore(
                brand_name=brand_name,
                brand_normalized=brand_normalized,
                date=date,
                platform=platform,
                score=round(final_score, 2),
                mention_count=mention_count,
                avg_position=round(avg_position or 0, 2),
                avg_sentiment=round(avg_sentiment or 0, 2),
                frequency_score=round(frequency_score * 100, 2),
                position_score=round(position_score * 100, 2),
                sentiment_score=round(sentiment_score * 100, 2),
                conversation_count=total_conversations,
            )
            db.add(visibility_score)
            scores.append(visibility_score)
        
        await db.commit()
        return scores
    
    def _calculate_frequency_score(
        self, mention_count: int, total_conversations: int
    ) -> float:
        """
        Calculate frequency score based on mention rate.
        
        Uses logarithmic scaling to prevent very high mention counts
        from dominating the score.
        """
        if total_conversations == 0:
            return 0.0
        
        # Mention rate (mentions per conversation)
        rate = mention_count / total_conversations
        
        # Logarithmic scaling with base adjustment
        # Score approaches 1.0 as rate increases
        score = min(1.0, math.log1p(rate * 10) / math.log1p(10))
        
        return score
    
    def _calculate_position_score(self, avg_position: float) -> float:
        """
        Calculate position score.
        
        Earlier positions (lower numbers) score higher.
        Position 0 = 1.0, Position 1000+ = ~0.1
        """
        # Inverse exponential decay
        # Position 0 -> 1.0, Position 500 -> ~0.5, Position 1000+ -> ~0.1
        score = math.exp(-avg_position / 500)
        return max(0.1, score)
    
    def _calculate_sentiment_score(self, avg_sentiment: float) -> float:
        """
        Calculate sentiment score.
        
        Sentiment ranges from -1 to 1, normalized to 0-1 for scoring.
        """
        # Normalize from [-1, 1] to [0, 1]
        return (avg_sentiment + 1) / 2
    
    async def _calculate_type_score(
        self,
        db: AsyncSession,
        brand_normalized: str,
        start_date: datetime,
        end_date: datetime,
    ) -> float:
        """
        Calculate type score based on mention type distribution.
        
        Recommendations and direct mentions score higher than
        comparisons or negative mentions.
        """
        # Get mention type breakdown
        query = (
            select(
                BrandMention.mention_type,
                func.count(BrandMention.id).label('count')
            )
            .where(BrandMention.brand_normalized == brand_normalized)
            .where(BrandMention.created_at >= start_date)
            .where(BrandMention.created_at < end_date)
            .group_by(BrandMention.mention_type)
        )
        
        result = await db.execute(query)
        type_counts = {row[0]: row[1] for row in result.all()}
        
        if not type_counts:
            return 0.5  # Default neutral score
        
        # Calculate weighted average
        total_count = sum(type_counts.values())
        weighted_sum = sum(
            self.TYPE_MULTIPLIERS.get(mention_type, 1.0) * count
            for mention_type, count in type_counts.items()
        )
        
        # Normalize to 0-1 range
        # Max possible is 1.5 (all recommendations), min is 0.3 (all negative)
        avg_multiplier = weighted_sum / total_count
        score = (avg_multiplier - 0.3) / (1.5 - 0.3)
        
        return max(0, min(1, score))
    
    async def calculate_rankings(
        self,
        db: AsyncSession,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict]:
        """
        Calculate brand rankings based on visibility scores.
        
        Args:
            db: Database session
            start_date: Start of period
            end_date: End of period
            category: Optional category filter
            limit: Maximum brands to return
            
        Returns:
            List of brand rankings with scores and trends
        """
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Get latest scores for each brand
        subquery = (
            select(
                VisibilityScore.brand_normalized,
                func.max(VisibilityScore.date).label('latest_date')
            )
            .where(VisibilityScore.date >= start_date)
            .where(VisibilityScore.date <= end_date)
            .group_by(VisibilityScore.brand_normalized)
            .subquery()
        )
        
        query = (
            select(VisibilityScore)
            .join(
                subquery,
                and_(
                    VisibilityScore.brand_normalized == subquery.c.brand_normalized,
                    VisibilityScore.date == subquery.c.latest_date
                )
            )
            .order_by(desc(VisibilityScore.score))
            .limit(limit)
        )
        
        result = await db.execute(query)
        scores = result.scalars().all()
        
        # Build rankings with trend calculation
        rankings = []
        for rank, score in enumerate(scores, 1):
            # Calculate trend (compare to previous period)
            trend = await self._calculate_trend(
                db, score.brand_normalized, start_date, end_date
            )
            
            rankings.append({
                'rank': rank,
                'brand_name': score.brand_name,
                'brand_normalized': score.brand_normalized,
                'score': score.score,
                'mention_count': score.mention_count,
                'avg_sentiment': score.avg_sentiment,
                'trend': trend['direction'],
                'trend_change': trend['change'],
            })
        
        return rankings
    
    async def _calculate_trend(
        self,
        db: AsyncSession,
        brand_normalized: str,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict:
        """
        Calculate trend direction and change percentage.
        
        Compares current period to previous period of same length.
        """
        period_length = (end_date - start_date).days
        prev_start = start_date - timedelta(days=period_length)
        prev_end = start_date
        
        # Get current period average score
        current_result = await db.execute(
            select(func.avg(VisibilityScore.score))
            .where(VisibilityScore.brand_normalized == brand_normalized)
            .where(VisibilityScore.date >= start_date)
            .where(VisibilityScore.date <= end_date)
        )
        current_avg = current_result.scalar() or 0
        
        # Get previous period average score
        prev_result = await db.execute(
            select(func.avg(VisibilityScore.score))
            .where(VisibilityScore.brand_normalized == brand_normalized)
            .where(VisibilityScore.date >= prev_start)
            .where(VisibilityScore.date < prev_end)
        )
        prev_avg = prev_result.scalar() or 0
        
        # Calculate change
        if prev_avg > 0:
            change = ((current_avg - prev_avg) / prev_avg) * 100
        else:
            change = 100 if current_avg > 0 else 0
        
        # Determine direction
        if change > 5:
            direction = 'up'
        elif change < -5:
            direction = 'down'
        else:
            direction = 'stable'
        
        return {
            'direction': direction,
            'change': round(change, 1),
        }


# Global calculator instance
visibility_calculator = VisibilityCalculator()
