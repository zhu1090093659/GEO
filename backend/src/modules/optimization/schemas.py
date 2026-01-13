"""
Optimization Module - API Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# Request Schemas

class GenerateRecommendationsRequest(BaseModel):
    """Request to generate recommendations"""
    brand: str
    focus_areas: Optional[List[str]] = None  # content, structure, technical


class LlmsTxtGenerateRequest(BaseModel):
    """Request to generate llms.txt"""
    url: str = Field(..., description="Website URL")
    site_name: str = Field(..., description="Site/organization name")
    description: Optional[str] = None
    auto_generate: bool = Field(default=True, description="Auto-discover sections")
    sections: Optional[List[dict]] = None


class UpdateRecommendationStatus(BaseModel):
    """Update recommendation status"""
    status: str = Field(..., description="pending, in_progress, completed, dismissed")


# Response Schemas

class RecommendationItem(BaseModel):
    """Single recommendation in response"""
    id: str
    category: str
    priority: str
    title: str
    description: str
    action_steps: List[str] = []
    expected_impact: str
    effort: str
    status: str


class RecommendationsResponse(BaseModel):
    """Recommendations list response"""
    brand: str
    generated_at: datetime
    recommendations: List[RecommendationItem] = []
    summary: dict = {}


class LlmsTxtResponse(BaseModel):
    """Generated llms.txt response"""
    url: str
    content: str
    preview_url: str
    download_url: str
    sections_count: int
    created_at: datetime
