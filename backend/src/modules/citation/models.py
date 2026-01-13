"""
Citation Module - Data Models
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Citation(BaseModel):
    """Citation extracted from AI response"""
    id: str
    conversation_id: str
    source_url: Optional[str] = None
    source_domain: Optional[str] = None
    source_name: Optional[str] = None
    citation_type: str = Field(..., description="url, domain, named, implicit")
    authority_score: float = Field(default=50.0, ge=0, le=100)
    context: str = Field(..., description="Surrounding text context")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WebsiteAnalysis(BaseModel):
    """Website analysis result"""
    id: str
    url: str
    domain: str
    status: str = Field(default="pending", description="pending, processing, completed, failed")
    citation_count: int = 0
    avg_sentiment: float = 0.0
    recommendations: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class CitationContext(BaseModel):
    """Context where a website was cited"""
    query: str
    response_snippet: str
    sentiment: float
    citation_type: str
    timestamp: datetime
