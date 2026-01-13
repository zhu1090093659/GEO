"""
Citation Module - Citation Discovery and Website Analysis
"""

from .service import CitationService
from .router import router as citation_router

__all__ = ["CitationService", "citation_router"]
