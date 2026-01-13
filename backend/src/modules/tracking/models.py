"""
Tracking Module - Database Models
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ConversationBase(BaseModel):
    """Base conversation data from extension"""
    query: str = Field(..., description="User's query to AI")
    response: str = Field(..., description="AI's response")
    platform: str = Field(..., description="Platform identifier (chatgpt, claude)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    language: Optional[str] = None
    region: Optional[str] = None


class Conversation(ConversationBase):
    """Conversation with ID"""
    id: str = Field(..., description="Unique conversation ID")


class BrandMention(BaseModel):
    """Brand mention extracted from conversation"""
    id: str
    conversation_id: str
    brand_name: str
    mention_type: str = Field(..., description="direct, indirect, comparison, negative")
    position: int = Field(..., description="Position in response (0-indexed)")
    sentiment: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score")
    context: str = Field(..., description="Surrounding text context")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VisibilityScore(BaseModel):
    """Calculated visibility score for a brand"""
    id: str
    brand_name: str
    date: datetime
    score: float = Field(..., ge=0, le=100, description="Visibility score 0-100")
    mention_count: int
    avg_position: float
    avg_sentiment: float
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RankingData(BaseModel):
    """Brand ranking compared to competitors"""
    brand_name: str
    score: float
    rank: int
    mention_count: int
    trend: str = Field(..., description="up, down, stable")
