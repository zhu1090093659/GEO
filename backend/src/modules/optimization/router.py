"""
Optimization Module - API Routes
"""

from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import PlainTextResponse

from .schemas import (
    GenerateRecommendationsRequest,
    LlmsTxtGenerateRequest,
    UpdateRecommendationStatus,
    RecommendationsResponse,
    RecommendationItem,
    LlmsTxtResponse,
)
from .service import optimization_service

router = APIRouter(prefix="/optimization", tags=["optimization"])


# Recommendations endpoints

@router.post("/recommendations", response_model=RecommendationsResponse)
async def generate_recommendations(request: GenerateRecommendationsRequest):
    """
    Generate optimization recommendations for a brand.
    
    Returns actionable recommendations based on visibility analysis.
    """
    return await optimization_service.generate_recommendations(
        request.brand,
        request.focus_areas,
    )


@router.get("/recommendations", response_model=List[RecommendationItem])
async def get_recommendations(
    brand: str = Query(..., description="Brand name"),
):
    """
    Get existing recommendations for a brand.
    """
    return await optimization_service.get_recommendations(brand)


@router.patch("/recommendations/{recommendation_id}")
async def update_recommendation_status(
    recommendation_id: str,
    request: UpdateRecommendationStatus,
):
    """
    Update recommendation status.
    
    Track progress on implementing recommendations.
    """
    success = await optimization_service.update_recommendation_status(
        recommendation_id,
        request.status,
    )
    if not success:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"success": True}


# llms.txt endpoints

@router.post("/llms-txt", response_model=LlmsTxtResponse)
async def generate_llms_txt(request: LlmsTxtGenerateRequest):
    """
    Generate llms.txt content for a website.
    
    Returns generated content with preview and download links.
    """
    return await optimization_service.generate_llms_txt(
        url=request.url,
        site_name=request.site_name,
        description=request.description,
        auto_generate=request.auto_generate,
        sections=request.sections,
    )


@router.get("/llms-txt/{result_id}/preview")
async def preview_llms_txt(result_id: str):
    """
    Preview generated llms.txt content.
    """
    result = await optimization_service.get_llms_txt(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return PlainTextResponse(result.content)


@router.get("/llms-txt/{result_id}/download")
async def download_llms_txt(result_id: str):
    """
    Download generated llms.txt file.
    """
    result = await optimization_service.get_llms_txt(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return PlainTextResponse(
        result.content,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=llms.txt"},
    )
