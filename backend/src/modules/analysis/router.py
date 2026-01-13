"""
Analysis Module - API Routes
"""

from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException

from .schemas import (
    AddCompetitorRequest,
    CompetitorComparisonResponse,
    SentimentResponse,
    TopicDiscoveryResponse,
)
from .service import analysis_service

router = APIRouter(prefix="/analysis", tags=["analysis"])


# Competitor endpoints

@router.post("/competitors")
async def add_competitor(request: AddCompetitorRequest):
    """Add a competitor to track"""
    competitor = await analysis_service.add_competitor(request.name, request.category)
    return {"success": True, "competitor": competitor}


@router.get("/competitors")
async def list_competitors():
    """List all tracked competitors"""
    competitors = await analysis_service.get_competitors()
    return {"competitors": competitors}


@router.delete("/competitors/{competitor_id}")
async def remove_competitor(competitor_id: str):
    """Remove a competitor from tracking"""
    success = await analysis_service.remove_competitor(competitor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return {"success": True}


@router.get("/competitors/compare", response_model=CompetitorComparisonResponse)
async def compare_competitors(
    brand: str = Query(..., description="Brand name to compare"),
    competitors: Optional[str] = Query(None, description="Comma-separated competitor names"),
):
    """
    Compare brand visibility against competitors.
    
    Returns ranking and visibility comparison data.
    """
    competitor_list = competitors.split(",") if competitors else None
    return await analysis_service.compare_competitors(brand, competitor_list)


# Sentiment endpoints

@router.get("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(
    brand: str = Query(..., description="Brand name to analyze"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
):
    """
    Analyze sentiment for a brand in AI responses.
    
    Returns overall sentiment score, distribution, and sample responses.
    """
    return await analysis_service.analyze_sentiment(brand, start_date, end_date)


# Topic discovery endpoints

@router.get("/topics", response_model=TopicDiscoveryResponse)
async def discover_topics(
    brand: Optional[str] = Query(None, description="Optional brand filter"),
    limit: int = Query(20, le=50, description="Maximum topics"),
):
    """
    Discover trending topics and keywords from queries.
    
    Returns popular topics, keywords, and trends.
    """
    return await analysis_service.discover_topics(brand, limit)
