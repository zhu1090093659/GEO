"""
Analysis Module - Business Logic Service
"""

from datetime import datetime, timedelta
from typing import List, Optional
import uuid

from .models import Competitor, SentimentResult, Topic, Keyword
from .schemas import (
    CompetitorComparisonResponse,
    CompetitorItem,
    SentimentResponse,
    SentimentDistribution,
    SentimentSample,
    TopicDiscoveryResponse,
    TopicItem,
    KeywordItem,
)


class AnalysisService:
    """Service for competitor, sentiment, and topic analysis"""

    def __init__(self):
        # In-memory storage for MVP
        self._competitors: List[Competitor] = []
        self._topics: List[Topic] = []
        self._keywords: List[Keyword] = []

    async def add_competitor(self, name: str, category: Optional[str] = None) -> Competitor:
        """Add a competitor to track"""
        competitor = Competitor(
            id=str(uuid.uuid4()),
            name=name,
            category=category,
        )
        self._competitors.append(competitor)
        return competitor

    async def get_competitors(self) -> List[Competitor]:
        """Get all tracked competitors"""
        return self._competitors

    async def remove_competitor(self, competitor_id: str) -> bool:
        """Remove a competitor from tracking"""
        for i, c in enumerate(self._competitors):
            if c.id == competitor_id:
                self._competitors.pop(i)
                return True
        return False

    async def compare_competitors(
        self,
        brand: str,
        competitors: Optional[List[str]] = None,
    ) -> CompetitorComparisonResponse:
        """
        Compare brand visibility against competitors.
        
        Args:
            brand: Target brand name
            competitors: Optional list of competitor names
            
        Returns:
            Comparison data with rankings
        """
        # Use tracked competitors if not specified
        if not competitors:
            competitors = [c.name for c in self._competitors]

        # Placeholder comparison data (integrate with tracking module later)
        all_brands = [brand] + competitors
        comparison_items = []
        
        for i, b in enumerate(all_brands):
            comparison_items.append(
                CompetitorItem(
                    name=b,
                    visibility_score=50.0 + (len(all_brands) - i) * 10,
                    mention_count=100 - i * 10,
                    rank=i + 1,
                    sentiment=0.5 - i * 0.1,
                )
            )

        # Sort by score
        comparison_items.sort(key=lambda x: x.visibility_score, reverse=True)
        for i, item in enumerate(comparison_items):
            item.rank = i + 1

        # Find brand data
        brand_item = next((c for c in comparison_items if c.name.lower() == brand.lower()), None)

        return CompetitorComparisonResponse(
            brand=brand,
            brand_score=brand_item.visibility_score if brand_item else 0,
            brand_rank=brand_item.rank if brand_item else 0,
            competitors=[c for c in comparison_items if c.name.lower() != brand.lower()],
            analysis_date=datetime.utcnow(),
        )

    async def analyze_sentiment(
        self,
        brand: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> SentimentResponse:
        """
        Analyze sentiment for a brand in AI responses.
        
        Args:
            brand: Brand name to analyze
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            Sentiment analysis results
        """
        # Placeholder sentiment data (integrate with Claude API later)
        overall_sentiment = 0.65
        
        if overall_sentiment > 0.3:
            label = "positive"
        elif overall_sentiment < -0.3:
            label = "negative"
        else:
            label = "neutral"

        return SentimentResponse(
            brand=brand,
            overall_sentiment=overall_sentiment,
            sentiment_label=label,
            distribution=SentimentDistribution(
                positive=60.0,
                neutral=30.0,
                negative=10.0,
            ),
            trend=[
                {"date": (datetime.utcnow() - timedelta(days=i)).isoformat(), "sentiment": 0.6 + i * 0.01}
                for i in range(7, 0, -1)
            ],
            samples=[
                SentimentSample(
                    query="What is the best CRM software?",
                    response_snippet=f"...{brand} is known for its excellent features...",
                    sentiment_score=0.8,
                    sentiment_label="positive",
                ),
            ],
        )

    async def discover_topics(
        self,
        brand: Optional[str] = None,
        limit: int = 20,
    ) -> TopicDiscoveryResponse:
        """
        Discover trending topics and keywords from queries.
        
        Args:
            brand: Optional brand to filter topics
            limit: Maximum topics to return
            
        Returns:
            Discovered topics and keywords
        """
        # Placeholder topic data (integrate with Claude API later)
        topics = [
            TopicItem(
                name="Product Comparison",
                query_count=150,
                keywords=["best", "vs", "compare", "alternative"],
                trend="up",
                growth_rate=15.5,
            ),
            TopicItem(
                name="Pricing",
                query_count=120,
                keywords=["price", "cost", "free", "subscription"],
                trend="stable",
                growth_rate=2.0,
            ),
            TopicItem(
                name="Features",
                query_count=100,
                keywords=["features", "capabilities", "integration"],
                trend="up",
                growth_rate=10.0,
            ),
        ]

        keywords = [
            KeywordItem(word="best", count=200, trend="up", related_brands=[]),
            KeywordItem(word="review", count=150, trend="stable", related_brands=[]),
            KeywordItem(word="alternative", count=100, trend="up", related_brands=[]),
        ]

        return TopicDiscoveryResponse(
            topics=topics[:limit],
            keywords=keywords[:limit],
            total_queries_analyzed=1000,
            analysis_period="Last 30 days",
        )


# Global service instance
analysis_service = AnalysisService()
