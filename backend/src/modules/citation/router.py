"""
Citation Module - API Routes
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException

from .schemas import (
    WebsiteAnalyzeRequest,
    CitationDiscoveryResponse,
    WebsiteAnalysisResponse,
    AnalysisStatusResponse,
)
from .service import citation_service

router = APIRouter(prefix="/citation", tags=["citation"])


@router.get("/discover", response_model=CitationDiscoveryResponse)
async def discover_citations(
    brand: Optional[str] = Query(None, description="Optional brand filter"),
    limit: int = Query(50, le=100, description="Maximum results"),
):
    """
    Discover citations from collected AI responses.
    
    Returns sources that AI frequently cites, with authority scores.
    """
    return await citation_service.discover_citations(brand, limit)


@router.post("/analyze", response_model=WebsiteAnalysisResponse)
async def analyze_website(request: WebsiteAnalyzeRequest):
    """
    Analyze a website for AI citation presence.
    
    Returns how often the website is cited, in what context,
    and recommendations for improvement.
    """
    return await citation_service.analyze_website(request.url, request.depth)


@router.get("/analyze/{analysis_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(analysis_id: str):
    """
    Get status of website analysis.
    
    Poll this endpoint to check analysis progress.
    """
    result = await citation_service.get_analysis_status(analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result
