"""
Citation Module - API Schemas (Pydantic)

Request/Response schemas for citation discovery
and website analysis APIs.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================
# Request Schemas
# ============================================

class WebsiteAnalyzeRequest(BaseModel):
    """Request to analyze a website for AI citation presence."""
    url: str = Field(..., description="Website URL to analyze")
    depth: int = Field(default=1, ge=1, le=5, description="Number of pages to analyze")
    force_refresh: bool = Field(default=False, description="Bypass cache")


class CitationExtractRequest(BaseModel):
    """Request to extract citations from text."""
    text: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    message_id: Optional[int] = None


# ============================================
# Response Schemas
# ============================================

class CitationItem(BaseModel):
    """Individual citation in response."""
    id: int
    source_url: Optional[str]
    source_domain: Optional[str]
    source_name: Optional[str]
    citation_type: str
    authority_score: float
    confidence: float
    context: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class CitationSourceItem(BaseModel):
    """Aggregated citation source statistics."""
    id: int
    domain: str
    display_name: Optional[str]
    source_type: str
    authority_score: float
    citation_count: int
    avg_sentiment: float
    first_cited_at: datetime
    last_cited_at: datetime
    is_verified: bool
    
    class Config:
        from_attributes = True


class CitationDiscoveryResponse(BaseModel):
    """Citation discovery results."""
    total_citations: int
    total_sources: int
    sources: List[CitationSourceItem] = Field(default_factory=list)
    top_domains: List[Dict[str, Any]] = Field(default_factory=list)
    by_type: Dict[str, int] = Field(default_factory=dict)
    by_source_type: Dict[str, int] = Field(default_factory=dict)
    period: str


class CitationContextItem(BaseModel):
    """Context where a website was cited."""
    query: str
    response_snippet: str
    sentiment: float
    citation_type: str
    platform: Optional[str]
    timestamp: datetime


class WebsiteRecommendation(BaseModel):
    """Optimization recommendation for improving AI visibility."""
    category: str = Field(..., description="content, technical, seo, structure")
    title: str
    description: str
    priority: str = Field(..., description="P0, P1, P2")
    impact: str = Field(default="medium", description="high, medium, low")
    effort: str = Field(default="medium", description="high, medium, low")


class WebsiteAnalysisResponse(BaseModel):
    """Website analysis results."""
    id: int
    url: str
    domain: str
    status: str
    progress: int
    citation_count: int
    avg_sentiment: float
    citation_contexts: List[CitationContextItem] = Field(default_factory=list)
    recommendations: List[WebsiteRecommendation] = Field(default_factory=list)
    pages_analyzed: int
    started_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnalysisStatusResponse(BaseModel):
    """Analysis status check response."""
    id: int
    status: str
    progress: int
    estimated_time_seconds: Optional[int] = None
    result: Optional[WebsiteAnalysisResponse] = None


class CitationStatsResponse(BaseModel):
    """Overall citation statistics."""
    total_citations: int
    total_sources: int
    total_analyses: int
    top_source_types: Dict[str, int]
    top_citation_types: Dict[str, int]
    avg_authority_score: float
    recent_citations_count: int  # Last 24 hours


class ExtractCitationsResponse(BaseModel):
    """Response from citation extraction."""
    citations_found: int
    citations: List[CitationItem] = Field(default_factory=list)
    sources_updated: int
