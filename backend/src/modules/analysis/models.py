"""
Analysis Module - Data Models
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Competitor(BaseModel):
    """Competitor brand configuration"""
    id: str
    name: str
    category: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)


class CompetitorAnalysis(BaseModel):
    """Competitor analysis result"""
    brand_name: str
    visibility_score: float
    mention_count: int
    rank: int
    sentiment_avg: float
    top_contexts: List[str] = []


class SentimentResult(BaseModel):
    """Sentiment analysis result for a brand"""
    brand_name: str
    overall_sentiment: float = Field(..., ge=-1.0, le=1.0)
    sentiment_label: str = Field(..., description="positive, neutral, negative")
    distribution: dict = Field(default_factory=dict)  # {positive: %, neutral: %, negative: %}
    key_phrases: List[str] = []
    sample_responses: List[dict] = []


class Topic(BaseModel):
    """Discovered topic from queries"""
    id: str
    name: str
    query_count: int
    keywords: List[str] = []
    trend: str = Field(default="stable", description="up, down, stable")
    first_seen: datetime
    last_seen: datetime


class Keyword(BaseModel):
    """Trending keyword"""
    word: str
    count: int
    trend: str = Field(default="stable")
    related_topics: List[str] = []
