"""
Tracking Module - API Routes

Endpoints for conversation upload, visibility queries,
brand ranking, and score calculation.
"""
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from .schemas import (
    ConversationUploadRequest,
    UploadResponse,
    VisibilityResponse,
    RankingResponse,
    StatsResponse,
    BrandCreateRequest,
    BrandResponse,
)
from .service import tracking_service

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_conversations(
    request: ConversationUploadRequest,
    db: AsyncSession = Depends(get_db)
) -> UploadResponse:
    """
    Upload conversation data from browser extension.
    
    Receives batch of conversations captured by the extension,
    processes them to extract brand mentions and calculate visibility.
    """
    return await tracking_service.upload_conversations(db, request.conversations)


@router.get("/visibility", response_model=VisibilityResponse)
async def get_visibility(
    brand: str = Query(..., description="Brand name to query"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    platform: Optional[str] = Query(None, description="Platform filter (chatgpt, claude)"),
    db: AsyncSession = Depends(get_db)
) -> VisibilityResponse:
    """
    Get visibility data for a brand.
    
    Returns current visibility score, historical trend,
    and mention statistics.
    """
    return await tracking_service.get_visibility(
        db, brand, start_date, end_date, platform
    )


@router.get("/ranking", response_model=RankingResponse)
async def get_ranking(
    brand: str = Query(..., description="Brand name to query"),
    competitors: Optional[str] = Query(None, description="Comma-separated competitor names"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    limit: int = Query(10, le=50, description="Maximum results"),
    db: AsyncSession = Depends(get_db)
) -> RankingResponse:
    """
    Get ranking data for a brand compared to competitors.
    
    Returns the brand's rank among competitors
    based on visibility scores.
    """
    competitor_list = competitors.split(",") if competitors else None
    return await tracking_service.get_ranking(
        db, brand, competitor_list, start_date, end_date, limit
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_db)
) -> StatsResponse:
    """
    Get overall tracking statistics.
    
    Returns counts of conversations, messages, mentions,
    and tracked brands.
    """
    return await tracking_service.get_stats(db)


@router.post("/brands", response_model=BrandResponse)
async def register_brand(
    request: BrandCreateRequest,
    db: AsyncSession = Depends(get_db)
) -> BrandResponse:
    """
    Register a brand for tracking.
    
    Brands must be registered before they can be detected
    in AI responses.
    """
    import json
    
    brand = await tracking_service.register_brand(
        db,
        name=request.name,
        category=request.category,
        description=request.description,
        website=request.website,
        aliases=request.aliases,
        is_competitor=request.is_competitor,
    )
    
    return BrandResponse(
        id=brand.id,
        name=brand.name,
        category=brand.category,
        description=brand.description,
        website=brand.website,
        aliases=json.loads(brand.aliases) if brand.aliases else None,
        is_competitor=brand.is_competitor,
        is_active=brand.is_active,
        created_at=brand.created_at,
    )


@router.get("/brands", response_model=List[BrandResponse])
async def list_brands(
    include_competitors: bool = Query(True, description="Include competitor brands"),
    db: AsyncSession = Depends(get_db)
) -> List[BrandResponse]:
    """
    List all registered brands.
    """
    from sqlalchemy import select
    from .models import Brand
    import json
    
    query = select(Brand).where(Brand.is_active == True)
    if not include_competitors:
        query = query.where(Brand.is_competitor == False)
    
    result = await db.execute(query.order_by(Brand.name))
    brands = result.scalars().all()
    
    return [
        BrandResponse(
            id=b.id,
            name=b.name,
            category=b.category,
            description=b.description,
            website=b.website,
            aliases=json.loads(b.aliases) if b.aliases else None,
            is_competitor=b.is_competitor,
            is_active=b.is_active,
            created_at=b.created_at,
        )
        for b in brands
    ]


@router.post("/calculate-scores")
async def calculate_scores(
    date: Optional[datetime] = Query(None, description="Date to calculate scores for"),
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger visibility score calculation.
    
    Calculates scores for all brands based on mentions in the specified date.
    If no date provided, calculates for today.
    """
    from .calculator import visibility_calculator
    
    scores = await visibility_calculator.calculate_daily_scores(db, date)
    
    return {
        "calculated": len(scores),
        "date": (date or datetime.utcnow()).strftime('%Y-%m-%d'),
        "scores": [
            {
                "brand": s.brand_name,
                "score": s.score,
                "mentions": s.mention_count,
            }
            for s in scores
        ]
    }


@router.get("/rankings")
async def get_rankings(
    start_date: Optional[datetime] = Query(None, description="Start date"),
    end_date: Optional[datetime] = Query(None, description="End date"),
    limit: int = Query(20, le=100, description="Maximum brands"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get brand rankings based on visibility scores.
    
    Returns top brands ranked by their visibility score
    with trend indicators.
    """
    from .calculator import visibility_calculator
    
    rankings = await visibility_calculator.calculate_rankings(
        db, start_date, end_date, limit=limit
    )
    
    return {
        "rankings": rankings,
        "total": len(rankings),
        "period": {
            "start": (start_date or (datetime.utcnow() - timedelta(days=30))).strftime('%Y-%m-%d'),
            "end": (end_date or datetime.utcnow()).strftime('%Y-%m-%d'),
        }
    }
