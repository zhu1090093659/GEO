"""
Analysis Module - API Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Request Schemas

class AddCompetitorRequest(BaseModel):
    """Add competitor to tracking"""
    name: str
    category: Optional[str] = None


class SentimentQueryParams(BaseModel):
    """Query parameters for sentiment API"""
    brand: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


# Response Schemas

class CompetitorItem(BaseModel):
    """Competitor in comparison"""
    name: str
    visibility_score: float
    mention_count: int
    rank: int
    sentiment: float


class CompetitorComparisonResponse(BaseModel):
    """Competitor comparison response"""
    brand: str
    brand_score: float
    brand_rank: int
    competitors: List[CompetitorItem] = []
    analysis_date: datetime


class SentimentDistribution(BaseModel):
    """Sentiment distribution breakdown"""
    positive: float
    neutral: float
    negative: float


class SentimentSample(BaseModel):
    """Sample response with sentiment"""
    query: str
    response_snippet: str
    sentiment_score: float
    sentiment_label: str


class SentimentResponse(BaseModel):
    """Sentiment analysis response"""
    brand: str
    overall_sentiment: float
    sentiment_label: str
    distribution: SentimentDistribution
    trend: List[dict] = []
    samples: List[SentimentSample] = []


class TopicItem(BaseModel):
    """Topic in discovery results"""
    name: str
    query_count: int
    keywords: List[str] = []
    trend: str
    growth_rate: Optional[float] = None


class KeywordItem(BaseModel):
    """Keyword in discovery results"""
    word: str
    count: int
    trend: str
    related_brands: List[str] = []


class TopicDiscoveryResponse(BaseModel):
    """Topic and keyword discovery response"""
    topics: List[TopicItem] = []
    keywords: List[KeywordItem] = []
    total_queries_analyzed: int
    analysis_period: str
