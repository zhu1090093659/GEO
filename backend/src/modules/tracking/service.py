"""
Tracking Module - Business Logic Service
"""

from datetime import datetime, timedelta
from typing import List, Optional
import uuid

from .models import Conversation, BrandMention, VisibilityScore
from .schemas import (
    ConversationUploadItem,
    UploadResponse,
    VisibilityResponse,
    VisibilityTrendItem,
    RankingResponse,
    RankingItem,
)


class TrackingService:
    """Service for tracking brand visibility in AI responses"""

    def __init__(self):
        # In-memory storage for MVP (replace with database later)
        self._conversations: List[Conversation] = []
        self._mentions: List[BrandMention] = []
        self._scores: List[VisibilityScore] = []

    async def upload_conversations(
        self, items: List[ConversationUploadItem]
    ) -> UploadResponse:
        """
        Process uploaded conversation data from extension.
        
        Args:
            items: List of conversation items from browser extension
            
        Returns:
            Upload result with counts
        """
        processed = 0
        errors = []

        for item in items:
            try:
                conversation = Conversation(
                    id=item.id,
                    query=item.query,
                    response=item.response,
                    platform=item.platform,
                    timestamp=datetime.fromisoformat(item.timestamp.replace('Z', '+00:00')),
                    language=item.metadata.get('language') if item.metadata else None,
                    region=item.metadata.get('region') if item.metadata else None,
                )
                self._conversations.append(conversation)
                
                # Extract brand mentions (placeholder - use Claude API later)
                await self._extract_mentions(conversation)
                
                processed += 1
            except Exception as e:
                errors.append(f"Error processing {item.id}: {str(e)}")

        return UploadResponse(
            received=len(items),
            processed=processed,
            errors=errors,
        )

    async def _extract_mentions(self, conversation: Conversation) -> None:
        """
        Extract brand mentions from conversation.
        TODO: Implement using Claude API for NER.
        """
        # Placeholder implementation
        pass

    async def get_visibility(
        self,
        brand: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> VisibilityResponse:
        """
        Get visibility data for a brand.
        
        Args:
            brand: Brand name to query
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            Visibility data including score and trend
        """
        # Filter scores by date range
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()

        brand_scores = [
            s for s in self._scores
            if s.brand_name.lower() == brand.lower()
            and start_date <= s.date <= end_date
        ]

        # Calculate current and previous scores
        if brand_scores:
            current_score = brand_scores[-1].score
            previous_score = brand_scores[0].score if len(brand_scores) > 1 else None
            change_percent = (
                ((current_score - previous_score) / previous_score * 100)
                if previous_score and previous_score > 0
                else None
            )
            total_mentions = sum(s.mention_count for s in brand_scores)
        else:
            current_score = 0.0
            previous_score = None
            change_percent = None
            total_mentions = 0

        # Build trend data
        trend = [
            VisibilityTrendItem(
                date=s.date.isoformat(),
                score=s.score,
                mention_count=s.mention_count,
            )
            for s in brand_scores
        ]

        return VisibilityResponse(
            brand=brand,
            current_score=current_score,
            previous_score=previous_score,
            change_percent=change_percent,
            trend=trend,
            total_mentions=total_mentions,
        )

    async def get_ranking(
        self,
        brand: str,
        competitors: Optional[List[str]] = None,
        limit: int = 10,
    ) -> RankingResponse:
        """
        Get ranking data for a brand compared to competitors.
        
        Args:
            brand: Brand name to query
            competitors: Optional list of competitor names
            limit: Maximum number of results
            
        Returns:
            Ranking data with competitor comparison
        """
        # Get all brands to compare
        all_brands = set([brand])
        if competitors:
            all_brands.update(competitors)

        # Calculate rankings (placeholder data for MVP)
        rankings = []
        for i, b in enumerate(sorted(all_brands)):
            rankings.append(
                RankingItem(
                    brand_name=b,
                    score=50.0 + (i * 5),  # Placeholder scores
                    rank=i + 1,
                    mention_count=10 * (i + 1),
                    trend="stable",
                )
            )

        # Sort by score descending
        rankings.sort(key=lambda x: x.score, reverse=True)
        for i, r in enumerate(rankings):
            r.rank = i + 1

        # Find brand rank
        brand_item = next((r for r in rankings if r.brand_name.lower() == brand.lower()), None)
        brand_rank = brand_item.rank if brand_item else 0
        brand_score = brand_item.score if brand_item else 0.0

        return RankingResponse(
            brand=brand,
            brand_rank=brand_rank,
            brand_score=brand_score,
            competitors=[r for r in rankings if r.brand_name.lower() != brand.lower()][:limit],
            total_brands=len(rankings),
        )

    async def calculate_scores(self) -> None:
        """
        Calculate visibility scores for all brands.
        Called periodically by background task.
        """
        # Group mentions by brand
        brand_mentions: dict = {}
        for mention in self._mentions:
            if mention.brand_name not in brand_mentions:
                brand_mentions[mention.brand_name] = []
            brand_mentions[mention.brand_name].append(mention)

        # Calculate score for each brand
        for brand_name, mentions in brand_mentions.items():
            if not mentions:
                continue

            # Visibility score formula
            mention_count = len(mentions)
            avg_position = sum(m.position for m in mentions) / mention_count
            avg_sentiment = sum(m.sentiment for m in mentions) / mention_count

            # Score = base + position_bonus + sentiment_bonus
            position_weight = max(0, 1 - (avg_position / 10))  # Higher position = better
            sentiment_weight = (avg_sentiment + 1) / 2  # Normalize to 0-1

            score = min(100, max(0, (
                mention_count * 2 +  # Base from mentions
                position_weight * 30 +  # Position bonus
                sentiment_weight * 20  # Sentiment bonus
            )))

            self._scores.append(
                VisibilityScore(
                    id=str(uuid.uuid4()),
                    brand_name=brand_name,
                    date=datetime.utcnow(),
                    score=score,
                    mention_count=mention_count,
                    avg_position=avg_position,
                    avg_sentiment=avg_sentiment,
                )
            )


# Global service instance
tracking_service = TrackingService()
