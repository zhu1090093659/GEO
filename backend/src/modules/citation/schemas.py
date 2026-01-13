"""
Citation Module - API Schemas
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


# Request Schemas

class WebsiteAnalyzeRequest(BaseModel):
    """Request to analyze a website"""
    url: str = Field(..., description="Website URL to analyze")
    depth: int = Field(default=1, ge=1, le=5, description="Pages to analyze")


# Response Schemas

class CitationSourceItem(BaseModel):
    """Citation source in results"""
    source: str
    source_type: str
    citation_count: int
    authority_score: float
    sample_context: Optional[str] = None


class CitationDiscoveryResponse(BaseModel):
    """Citation discovery results"""
    total_citations: int
    sources: List[CitationSourceItem] = []
    top_domains: List[dict] = []
    by_type: dict = {}


class CitationContextItem(BaseModel):
    """Context where website was cited"""
    query: str
    response_snippet: str
    sentiment: float
    timestamp: str


class WebsiteRecommendation(BaseModel):
    """Optimization recommendation for website"""
    category: str
    title: str
    description: str
    priority: str


class WebsiteAnalysisResponse(BaseModel):
    """Website analysis results"""
    url: str
    status: str
    analysis_id: Optional[str] = None
    citation_count: int = 0
    sentiment_avg: float = 0.0
    citation_contexts: List[CitationContextItem] = []
    recommendations: List[WebsiteRecommendation] = []
    completed_at: Optional[datetime] = None


class AnalysisStatusResponse(BaseModel):
    """Analysis status check response"""
    analysis_id: str
    status: str
    progress: Optional[int] = None
    estimated_time: Optional[int] = None
    result: Optional[WebsiteAnalysisResponse] = None
