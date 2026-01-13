"""
Tracking Module - API Schemas (Pydantic)

Request/Response schemas for the tracking API.
Separate from SQLAlchemy models for clean API contracts.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ============================================
# Request Schemas
# ============================================

class MessageUploadItem(BaseModel):
    """Single message in a conversation upload."""
    role: str = Field(..., description="user or assistant")
    content: str
    timestamp: Optional[str] = None


class ConversationUploadItem(BaseModel):
    """Single conversation item for upload from extension."""
    id: str = Field(..., description="UUID from extension")
    session_id: str = Field(..., description="Browser session ID")
    platform: str = Field(..., description="chatgpt, claude, etc.")
    messages: List[MessageUploadItem]
    captured_at: str = Field(..., description="ISO timestamp when captured")
    metadata: Optional[dict] = None


class ConversationUploadRequest(BaseModel):
    """Batch upload request from extension."""
    conversations: List[ConversationUploadItem]


class VisibilityQueryParams(BaseModel):
    """Query parameters for visibility API."""
    brand: str = Field(..., min_length=1)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    platform: Optional[str] = None


class RankingQueryParams(BaseModel):
    """Query parameters for ranking API."""
    brand: str
    competitors: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=10, le=50)


class BrandCreateRequest(BaseModel):
    """Request to create/register a brand for tracking."""
    name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    aliases: Optional[List[str]] = None
    is_competitor: bool = False


# ============================================
# Response Schemas
# ============================================

class UploadResponse(BaseModel):
    """Response for conversation upload."""
    received: int = Field(..., description="Number of conversations received")
    processed: int = Field(..., description="Number successfully processed")
    brand_mentions_found: int = Field(default=0, description="Brands detected")
    errors: List[str] = Field(default_factory=list)


class MessageResponse(BaseModel):
    """Message in API response."""
    id: int
    role: str
    content: str
    sequence: int
    timestamp: Optional[datetime] = None


class ConversationResponse(BaseModel):
    """Conversation in API response."""
    id: str
    session_id: str
    platform: str
    initial_query: str
    captured_at: datetime
    message_count: int
    brand_mentions_count: int


class BrandMentionResponse(BaseModel):
    """Brand mention in API response."""
    id: int
    brand_name: str
    mention_type: str
    position: int
    context: str
    sentiment: float
    confidence: float
    message_id: int


class ConversationDetailResponse(BaseModel):
    """Detailed conversation with messages."""
    id: str
    session_id: str
    platform: str
    initial_query: str
    captured_at: datetime
    messages: List[MessageResponse]
    brand_mentions: List[BrandMentionResponse]


class VisibilityTrendItem(BaseModel):
    """Single point in visibility trend."""
    date: str
    score: float
    mention_count: int
    sentiment: float


class VisibilityResponse(BaseModel):
    """Visibility data response."""
    brand: str
    current_score: float = Field(..., description="Current visibility score 0-100")
    previous_score: Optional[float] = None
    change_percent: Optional[float] = None
    trend: List[VisibilityTrendItem] = Field(default_factory=list)
    total_mentions: int
    avg_sentiment: float
    period_days: int


class RankingItem(BaseModel):
    """Single brand in ranking."""
    brand_name: str
    score: float
    rank: int
    mention_count: int
    trend: str = Field(..., description="up, down, or stable")
    change: Optional[int] = None


class RankingResponse(BaseModel):
    """Ranking data response."""
    brand: str
    brand_rank: int
    brand_score: float
    rankings: List[RankingItem] = Field(default_factory=list)
    total_brands: int
    period: str


class BrandResponse(BaseModel):
    """Brand in API response."""
    id: int
    name: str
    category: Optional[str]
    description: Optional[str]
    website: Optional[str]
    aliases: Optional[List[str]]
    is_competitor: bool
    is_active: bool
    created_at: datetime


class StatsResponse(BaseModel):
    """Overall tracking statistics."""
    total_conversations: int
    total_messages: int
    total_brand_mentions: int
    total_brands_tracked: int
    platforms: dict
    date_range: dict
