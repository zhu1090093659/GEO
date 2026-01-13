"""
Optimization Module - API Schemas (Pydantic)

Request/Response schemas for optimization recommendations
and llms.txt generation APIs.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================
# Request Schemas
# ============================================

class GenerateRecommendationsRequest(BaseModel):
    """Request to generate optimization recommendations."""
    brand: str = Field(..., min_length=1, description="Brand name")
    focus_areas: Optional[List[str]] = Field(
        None, 
        description="Filter by category: content, structure, technical, seo, branding"
    )
    include_completed: bool = Field(
        default=False, 
        description="Include previously completed recommendations"
    )


class LlmsTxtGenerateRequest(BaseModel):
    """Request to generate llms.txt content."""
    url: str = Field(..., description="Website URL")
    site_name: str = Field(..., description="Site/organization name")
    description: Optional[str] = Field(None, description="Site description")
    auto_generate: bool = Field(default=True, description="Auto-discover sections")
    sections: Optional[List[Dict[str, str]]] = Field(
        None, 
        description="Manual sections [{name, path, description}]"
    )
    topics: Optional[List[str]] = Field(None, description="Key topics")
    contact_email: Optional[str] = None


class UpdateRecommendationRequest(BaseModel):
    """Update recommendation status."""
    status: str = Field(
        ..., 
        description="Status: pending, in_progress, completed, dismissed"
    )
    notes: Optional[str] = Field(None, description="Implementation notes")


# ============================================
# Response Schemas
# ============================================

class RecommendationItem(BaseModel):
    """Single recommendation in response."""
    id: int
    brand: str
    category: str
    priority: str
    title: str
    description: str
    action_steps: List[str] = Field(default_factory=list)
    expected_impact: str
    effort: str
    impact_score: float
    status: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RecommendationSummary(BaseModel):
    """Summary statistics for recommendations."""
    total: int
    by_priority: Dict[str, int]
    by_category: Dict[str, int]
    by_status: Dict[str, int]
    avg_impact_score: float


class RecommendationsResponse(BaseModel):
    """Recommendations list response."""
    brand: str
    generated_at: datetime
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    summary: RecommendationSummary
    new_count: int = Field(default=0, description="Newly generated recommendations")


class LlmsTxtSection(BaseModel):
    """Section in llms.txt."""
    name: str
    path: str
    description: str


class LlmsTxtResponse(BaseModel):
    """Generated llms.txt response."""
    id: int
    url: str
    domain: str
    site_name: str
    content: str
    sections: List[LlmsTxtSection] = Field(default_factory=list)
    preview_url: str
    download_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class OptimizationStatsResponse(BaseModel):
    """Optimization module statistics."""
    total_recommendations: int
    recommendations_by_status: Dict[str, int]
    recommendations_by_category: Dict[str, int]
    recommendations_by_priority: Dict[str, int]
    total_llms_txt_generated: int
    avg_impact_score: float
    completion_rate: float