"""
Analysis Module - API Routes

Endpoints for competitor analysis, sentiment analysis,
and topic discovery.
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from .schemas import (
    AddCompetitorRequest,
    CreateCompetitorGroupRequest,
    UpdateCompetitorGroupRequest,
    CompetitorComparisonResponse,
    CompetitorGroupResponse,
    SentimentResponse,
    TopicDiscoveryResponse,
    AnalysisStatsResponse,
)
from .service import analysis_service

router = APIRouter()


# ========================================
# Competitor Group Endpoints
# ========================================

@router.post("/competitor-groups", response_model=CompetitorGroupResponse)
async def create_competitor_group(
    request: CreateCompetitorGroupRequest,
    db: AsyncSession = Depends(get_db)
) -> CompetitorGroupResponse:
    """
    Create a new competitor group.
    
    Groups allow organizing competitors by category or market segment
    for easier comparison analysis.
    """
    group = await analysis_service.create_competitor_group(
        db,
        name=request.name,
        description=request.description,
        category=request.category,
        owner_brand=request.owner_brand,
        competitor_names=request.competitor_names,
    )
    
    return CompetitorGroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        category=group.category,
        owner_brand=None,  # TODO: Get owner brand name
        competitors=[b.name for b in group.brands],
        is_active=group.is_active,
        created_at=group.created_at,
    )


@router.get("/competitor-groups", response_model=List[CompetitorGroupResponse])
async def list_competitor_groups(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db)
) -> List[CompetitorGroupResponse]:
    """
    List all competitor groups.
    
    Optionally filter by category.
    """
    groups = await analysis_service.get_competitor_groups(db, category)
    
    return [
        CompetitorGroupResponse(
            id=g.id,
            name=g.name,
            description=g.description,
            category=g.category,
            owner_brand=None,
            competitors=[b.name for b in g.brands],
            is_active=g.is_active,
            created_at=g.created_at,
        )
        for g in groups
    ]


@router.get("/competitor-groups/{group_id}", response_model=CompetitorGroupResponse)
async def get_competitor_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
) -> CompetitorGroupResponse:
    """Get a specific competitor group by ID."""
    group = await analysis_service.get_competitor_group(db, group_id)
    
    if not group:
        raise HTTPException(status_code=404, detail="Competitor group not found")
    
    return CompetitorGroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        category=group.category,
        owner_brand=None,
        competitors=[b.name for b in group.brands],
        is_active=group.is_active,
        created_at=group.created_at,
    )


@router.post("/competitor-groups/{group_id}/competitors")
async def add_competitor_to_group(
    group_id: int,
    request: AddCompetitorRequest,
    db: AsyncSession = Depends(get_db)
):
    """Add a competitor to an existing group."""
    success = await analysis_service.add_competitor_to_group(
        db, group_id, request.name
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Competitor group not found")
    
    return {"success": True, "message": f"Added {request.name} to group"}


@router.delete("/competitor-groups/{group_id}/competitors/{competitor_name}")
async def remove_competitor_from_group(
    group_id: int,
    competitor_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Remove a competitor from a group."""
    success = await analysis_service.remove_competitor_from_group(
        db, group_id, competitor_name
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Competitor not found in group")
    
    return {"success": True, "message": f"Removed {competitor_name} from group"}


@router.delete("/competitor-groups/{group_id}")
async def delete_competitor_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a competitor group."""
    success = await analysis_service.delete_competitor_group(db, group_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Competitor group not found")
    
    return {"success": True, "message": "Competitor group deleted"}


# ========================================
# Competitor Comparison Endpoints
# ========================================

@router.get("/competitors/compare", response_model=CompetitorComparisonResponse)
async def compare_competitors(
    brand: str = Query(..., description="Brand name to compare"),
    competitors: Optional[str] = Query(None, description="Comma-separated competitor names"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    db: AsyncSession = Depends(get_db)
) -> CompetitorComparisonResponse:
    """
    Compare brand visibility against competitors.
    
    Returns ranking and visibility comparison data.
    If no competitors specified, compares against all tracked competitors.
    """
    competitor_list = competitors.split(",") if competitors else None
    return await analysis_service.compare_competitors(
        db, brand, competitor_list, start_date, end_date
    )


# ========================================
# Sentiment Analysis Endpoints
# ========================================

@router.get("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(
    brand: str = Query(..., description="Brand name to analyze"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    db: AsyncSession = Depends(get_db)
) -> SentimentResponse:
    """
    Analyze sentiment for a brand in AI responses.
    
    Returns overall sentiment score, distribution, trend, and sample responses.
    """
    return await analysis_service.analyze_sentiment(db, brand, start_date, end_date)


# ========================================
# Topic Discovery Endpoints
# ========================================

@router.get("/topics", response_model=TopicDiscoveryResponse)
async def discover_topics(
    brand: Optional[str] = Query(None, description="Optional brand filter"),
    limit: int = Query(20, le=100, description="Maximum topics"),
    db: AsyncSession = Depends(get_db)
) -> TopicDiscoveryResponse:
    """
    Discover trending topics and keywords from queries.
    
    Returns popular topics, keywords, and trends.
    """
    return await analysis_service.discover_topics(db, brand, limit)


@router.post("/topics/extract")
async def extract_topics(
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    db: AsyncSession = Depends(get_db)
):
    """
    Extract topics and keywords from recent conversations.
    
    Triggers topic extraction analysis on conversation data.
    """
    result = await analysis_service.extract_topics_from_conversations(
        db, start_date, end_date
    )
    return {"success": True, **result}


@router.post("/keywords/cluster")
async def cluster_keywords(
    min_count: int = Query(5, ge=1, description="Minimum keyword count"),
    db: AsyncSession = Depends(get_db)
):
    """
    Cluster keywords into related groups.
    
    Groups similar keywords based on co-occurrence.
    """
    result = await analysis_service.cluster_keywords(db, min_count)
    return {"success": True, **result}


# ========================================
# Statistics Endpoint
# ========================================

@router.get("/stats", response_model=AnalysisStatsResponse)
async def get_analysis_stats(
    db: AsyncSession = Depends(get_db)
) -> AnalysisStatsResponse:
    """
    Get overall analysis statistics.
    
    Returns counts of competitor groups, analyses performed, etc.
    """
    return await analysis_service.get_stats(db)
