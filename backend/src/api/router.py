"""
API Router - aggregates all API routes
"""
from fastapi import APIRouter

from src.modules.chat.router import router as chat_router
from src.modules.tracking.router import router as tracking_router
from src.modules.analysis.router import router as analysis_router
from src.modules.citation.router import router as citation_router
from src.modules.optimization.router import router as optimization_router

api_router = APIRouter()


# Health check
@api_router.get("/ping")
async def ping():
    """Simple ping endpoint."""
    return {"message": "pong"}


@api_router.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "GEO API"}


# Chat routes (Agent interaction)
api_router.include_router(chat_router, tags=["chat"])

# GEO Core modules
api_router.include_router(tracking_router, prefix="/tracking", tags=["tracking"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
api_router.include_router(citation_router, prefix="/citation", tags=["citation"])
api_router.include_router(optimization_router, prefix="/optimization", tags=["optimization"])

