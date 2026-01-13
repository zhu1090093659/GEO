"""
Analysis Module - API Schemas (Pydantic)

Request/Response schemas for competitor analysis,
sentiment analysis, and topic discovery APIs.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================
# Request Schemas
# ============================================

class AddCompetitorRequest(BaseModel):
    """Add competitor to tracking."""
    name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = None


class CreateCompetitorGroupRequest(BaseModel):
    """Create a competitor group."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = None
    owner_brand: Optional[str] = None
    competitor_names: List[str] = Field(default_factory=list)


class UpdateCompetitorGroupRequest(BaseModel):
    """Update a competitor group."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    add_competitors: Optional[List[str]] = None
    remove_competitors: Optional[List[str]] = None


class SentimentQueryParams(BaseModel):
    """Query parameters for sentiment API."""
    brand: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    platform: Optional[str] = None


class TopicQueryParams(BaseModel):
    """Query parameters for topic discovery."""
    brand: Optional[str] = None
    category: Optional[str] = None
    limit: int = Field(default=20, le=100)
    min_count: int = Field(default=1, ge=1)


# ============================================
# Response Schemas
# ============================================

class CompetitorItem(BaseModel):
    """Competitor in comparison result."""
    name: str
    visibility_score: float
    mention_count: int
    rank: int
    sentiment: float
    trend: str = "stable"


class CompetitorGroupResponse(BaseModel):
    """Competitor group details."""
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    owner_brand: Optional[str]
    competitors: List[str]
    is_active: bool
    created_at: datetime


class CompetitorComparisonResponse(BaseModel):
    """Competitor comparison response."""
    brand: str
    brand_score: float
    brand_rank: int
    brand_mentions: int
    brand_sentiment: float
    competitors: List[CompetitorItem] = Field(default_factory=list)
    insights: Optional[str] = None
    analysis_date: datetime
    period: str


class ComparisonDetailResponse(BaseModel):
    """Detailed comparison between two brands."""
    brand: str
    competitor: str
    visibility_diff: float
    mention_diff: int
    sentiment_diff: float
    brand_metrics: Dict[str, Any]
    competitor_metrics: Dict[str, Any]
    insights: Optional[str] = None
    comparison_date: datetime


class SentimentDistribution(BaseModel):
    """Sentiment distribution breakdown."""
    positive: float = Field(..., ge=0, le=100)
    neutral: float = Field(..., ge=0, le=100)
    negative: float = Field(..., ge=0, le=100)


class SentimentSample(BaseModel):
    """Sample response with sentiment."""
    query: str
    response_snippet: str
    sentiment_score: float
    sentiment_label: str
    platform: Optional[str] = None
    timestamp: Optional[datetime] = None


class SentimentTrendItem(BaseModel):
    """Single point in sentiment trend."""
    date: str
    sentiment: float
    mention_count: int


class SentimentResponse(BaseModel):
    """Sentiment analysis response."""
    brand: str
    overall_sentiment: float = Field(..., ge=-1, le=1)
    sentiment_label: str
    distribution: SentimentDistribution
    trend: List[SentimentTrendItem] = Field(default_factory=list)
    samples: List[SentimentSample] = Field(default_factory=list)
    mentions_analyzed: int
    period_days: int


class TopicItem(BaseModel):
    """Topic in discovery results."""
    id: int
    name: str
    query_count: int
    keywords: List[str] = Field(default_factory=list)
    trend: str
    growth_rate: Optional[float] = None
    related_brands: List[str] = Field(default_factory=list)


class KeywordItem(BaseModel):
    """Keyword in discovery results."""
    word: str
    count: int
    trend: str
    growth_rate: Optional[float] = None
    related_topics: List[str] = Field(default_factory=list)
    related_brands: List[str] = Field(default_factory=list)


class TopicDiscoveryResponse(BaseModel):
    """Topic and keyword discovery response."""
    topics: List[TopicItem] = Field(default_factory=list)
    keywords: List[KeywordItem] = Field(default_factory=list)
    total_queries_analyzed: int
    analysis_period: str


class AnalysisStatsResponse(BaseModel):
    """Overall analysis statistics."""
    total_competitor_groups: int
    total_comparisons: int
    total_sentiment_analyses: int
    total_topics: int
    total_keywords: int
    last_analysis_date: Optional[datetime]
