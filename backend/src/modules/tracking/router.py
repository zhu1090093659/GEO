"""
Tracking Module - API Routes
"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException

from .schemas import (
    ConversationUploadRequest,
    UploadResponse,
    VisibilityResponse,
    RankingResponse,
)
from .service import tracking_service

router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.post("/upload", response_model=UploadResponse)
async def upload_conversations(request: ConversationUploadRequest) -> UploadResponse:
    """
    Upload conversation data from browser extension.
    
    Receives batch of conversations captured by the extension,
    processes them to extract brand mentions and calculate visibility.
    """
    return await tracking_service.upload_conversations(request.conversations)


@router.get("/visibility", response_model=VisibilityResponse)
async def get_visibility(
    brand: str = Query(..., description="Brand name to query"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
) -> VisibilityResponse:
    """
    Get visibility data for a brand.
    
    Returns current visibility score, historical trend,
    and mention statistics.
    """
    return await tracking_service.get_visibility(brand, start_date, end_date)


@router.get("/ranking", response_model=RankingResponse)
async def get_ranking(
    brand: str = Query(..., description="Brand name to query"),
    competitors: Optional[str] = Query(None, description="Comma-separated competitor names"),
    limit: int = Query(10, le=50, description="Maximum results"),
) -> RankingResponse:
    """
    Get ranking data for a brand compared to competitors.
    
    Returns the brand's rank among competitors
    based on visibility scores.
    """
    competitor_list = competitors.split(",") if competitors else None
    return await tracking_service.get_ranking(brand, competitor_list, limit)


@router.get("/stats")
async def get_stats():
    """
    Get overall tracking statistics.
    """
    return {
        "total_conversations": len(tracking_service._conversations),
        "total_mentions": len(tracking_service._mentions),
        "unique_brands": len(set(m.brand_name for m in tracking_service._mentions)),
    }
