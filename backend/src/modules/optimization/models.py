"""
Optimization Module - Data Models
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    """Optimization recommendation"""
    id: str
    brand: str
    category: str = Field(..., description="content, structure, technical")
    priority: str = Field(..., description="P0, P1, P2")
    title: str
    description: str
    action_steps: List[str] = []
    expected_impact: str
    effort: str = Field(..., description="low, medium, high")
    status: str = Field(default="pending", description="pending, in_progress, completed, dismissed")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LlmsTxtConfig(BaseModel):
    """Configuration for llms.txt generation"""
    site_name: str
    description: str
    url: str
    sections: List[dict] = []
    topics: List[str] = []
    contact_email: Optional[str] = None
    auto_generate: bool = True


class LlmsTxtResult(BaseModel):
    """Generated llms.txt result"""
    id: str
    url: str
    content: str
    preview_url: str
    download_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
