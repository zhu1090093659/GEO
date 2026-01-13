"""
Optimization Module - API Routes

Endpoints for optimization recommendations
and llms.txt generation.
"""
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db
from .schemas import (
    GenerateRecommendationsRequest,
    LlmsTxtGenerateRequest,
    UpdateRecommendationRequest,
    RecommendationsResponse,
    RecommendationItem,
    LlmsTxtResponse,
    OptimizationStatsResponse,
)
from .service import optimization_service

router = APIRouter()


# ========================================
# Recommendations Endpoints
# ========================================

@router.post("/recommendations", response_model=RecommendationsResponse)
async def generate_recommendations(
    request: GenerateRecommendationsRequest,
    db: AsyncSession = Depends(get_db),
) -> RecommendationsResponse:
    """
    Generate optimization recommendations for a brand.
    
    Returns actionable recommendations based on visibility analysis,
    citation data, and industry best practices.
    """
    return await optimization_service.generate_recommendations(
        db,
        request.brand,
        request.focus_areas,
        request.include_completed,
    )


@router.get("/recommendations", response_model=List[RecommendationItem])
async def get_recommendations(
    brand: str = Query(..., description="Brand name"),
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db),
) -> List[RecommendationItem]:
    """
    Get existing recommendations for a brand.
    
    Returns recommendations sorted by priority and impact score.
    """
    return await optimization_service.get_recommendations(
        db, brand, status, category
    )


@router.patch("/recommendations/{recommendation_id}", response_model=RecommendationItem)
async def update_recommendation_status(
    recommendation_id: int,
    request: UpdateRecommendationRequest,
    db: AsyncSession = Depends(get_db),
) -> RecommendationItem:
    """
    Update recommendation status.
    
    Track progress on implementing recommendations.
    Statuses: pending, in_progress, completed, dismissed
    """
    result = await optimization_service.update_recommendation_status(
        db,
        recommendation_id,
        request.status,
        request.notes,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return result


# ========================================
# llms.txt Endpoints
# ========================================

@router.post("/llms-txt", response_model=LlmsTxtResponse)
async def generate_llms_txt(
    request: LlmsTxtGenerateRequest,
    db: AsyncSession = Depends(get_db),
) -> LlmsTxtResponse:
    """
    Generate llms.txt content for a website.
    
    Returns generated content with preview and download links.
    The llms.txt format helps AI systems understand and index your content.
    """
    return await optimization_service.generate_llms_txt(
        db,
        url=request.url,
        site_name=request.site_name,
        description=request.description,
        auto_generate=request.auto_generate,
        sections=request.sections,
        topics=request.topics,
        contact_email=request.contact_email,
    )


@router.get("/llms-txt/{result_id}/preview")
async def preview_llms_txt(
    result_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Preview generated llms.txt content.
    
    Returns plain text preview of the generated file.
    """
    result = await optimization_service.get_llms_txt(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return PlainTextResponse(result.content)


@router.get("/llms-txt/{result_id}/download")
async def download_llms_txt(
    result_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Download generated llms.txt file.
    
    Returns file with proper content-disposition header for download.
    """
    result = await optimization_service.get_llms_txt(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return PlainTextResponse(
        result.content,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=llms.txt"},
    )


# ========================================
# Statistics Endpoint
# ========================================

@router.get("/stats", response_model=OptimizationStatsResponse)
async def get_optimization_stats(
    db: AsyncSession = Depends(get_db),
) -> OptimizationStatsResponse:
    """
    Get optimization module statistics.
    
    Returns recommendation counts, completion rates, and llms.txt stats.
    """
    return await optimization_service.get_stats(db)
