"""
Tracking Module - API Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Request Schemas

class ConversationUploadItem(BaseModel):
    """Single conversation item for upload"""
    id: str
    query: str
    response: str
    platform: str
    timestamp: str
    metadata: Optional[dict] = None


class ConversationUploadRequest(BaseModel):
    """Batch upload request from extension"""
    conversations: List[ConversationUploadItem]


class VisibilityQueryParams(BaseModel):
    """Query parameters for visibility API"""
    brand: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class RankingQueryParams(BaseModel):
    """Query parameters for ranking API"""
    brand: str
    competitors: Optional[List[str]] = None
    limit: int = Field(default=10, le=50)


# Response Schemas

class UploadResponse(BaseModel):
    """Response for conversation upload"""
    received: int
    processed: int
    errors: List[str] = []


class VisibilityTrendItem(BaseModel):
    """Single point in visibility trend"""
    date: str
    score: float
    mention_count: int


class VisibilityResponse(BaseModel):
    """Visibility data response"""
    brand: str
    current_score: float
    previous_score: Optional[float] = None
    change_percent: Optional[float] = None
    trend: List[VisibilityTrendItem] = []
    total_mentions: int


class RankingItem(BaseModel):
    """Single brand in ranking"""
    brand_name: str
    score: float
    rank: int
    mention_count: int
    trend: str


class RankingResponse(BaseModel):
    """Ranking data response"""
    brand: str
    brand_rank: int
    brand_score: float
    competitors: List[RankingItem] = []
    total_brands: int
