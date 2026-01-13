"""
Optimization Module - Optimization Recommendations and llms.txt Generation
"""

from .service import OptimizationService
from .router import router as optimization_router

__all__ = ["OptimizationService", "optimization_router"]
