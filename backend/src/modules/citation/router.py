"""
Citation Module - API Routes

Endpoints for citation discovery, extraction,
and website analysis.
"""
from typing import Optional
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from .schemas import (
    WebsiteAnalyzeRequest,
    CitationExtractRequest,
    CitationDiscoveryResponse,
    WebsiteAnalysisResponse,
    AnalysisStatusResponse,
    CitationStatsResponse,
    ExtractCitationsResponse,
)
from .service import citation_service

router = APIRouter()


# ========================================
# Citation Discovery Endpoints
# ========================================

@router.get("/discover", response_model=CitationDiscoveryResponse)
async def discover_citations(
    brand: Optional[str] = Query(None, description="Optional brand filter"),
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    limit: int = Query(50, le=100, description="Maximum results"),
    days: int = Query(30, ge=1, le=365, description="Period in days"),
    db: AsyncSession = Depends(get_db),
) -> CitationDiscoveryResponse:
    """
    Discover citations from collected AI responses.
    
    Returns sources that AI frequently cites, with authority scores
    and citation counts.
    """
    return await citation_service.discover_citations(
        db, brand, source_type, limit, days
    )


@router.post("/extract", response_model=ExtractCitationsResponse)
async def extract_citations(
    request: CitationExtractRequest,
    db: AsyncSession = Depends(get_db),
) -> ExtractCitationsResponse:
    """
    Extract citations from provided text.
    
    Useful for analyzing AI responses for citation presence.
    """
    return await citation_service.extract_citations_from_text(
        db,
        request.text,
        request.conversation_id,
        request.message_id,
    )


# ========================================
# Website Analysis Endpoints
# ========================================

@router.post("/analyze", response_model=WebsiteAnalysisResponse)
async def analyze_website(
    request: WebsiteAnalyzeRequest,
    db: AsyncSession = Depends(get_db),
) -> WebsiteAnalysisResponse:
    """
    Analyze a website for AI citation presence.
    
    Returns how often the website is cited, in what context,
    and recommendations for improvement.
    
    Results are cached for 24 hours unless force_refresh is true.
    """
    return await citation_service.analyze_website(
        db, request.url, request.depth, request.force_refresh
    )


@router.get("/analyze/{analysis_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(
    analysis_id: int,
    db: AsyncSession = Depends(get_db),
) -> AnalysisStatusResponse:
    """
    Get status of website analysis.
    
    Poll this endpoint to check analysis progress.
    Returns full results when completed.
    """
    result = await citation_service.get_analysis_status(db, analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result


# ========================================
# Statistics Endpoint
# ========================================

@router.get("/stats", response_model=CitationStatsResponse)
async def get_citation_stats(
    db: AsyncSession = Depends(get_db),
) -> CitationStatsResponse:
    """
    Get overall citation statistics.
    
    Returns counts of citations, sources, analyses,
    and distribution by type.
    """
    return await citation_service.get_stats(db)

