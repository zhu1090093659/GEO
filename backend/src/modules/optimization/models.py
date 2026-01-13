"""
Optimization Module - SQLAlchemy ORM Models

Database models for optimization recommendations
and llms.txt generation results.
"""
from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import (
    String, Text, Integer, Float, DateTime, Boolean, JSON, Index
)
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class RecommendationCategory(str, Enum):
    """Category of optimization recommendation."""
    CONTENT = "content"       # Content optimization
    STRUCTURE = "structure"   # Site structure/markup
    TECHNICAL = "technical"   # Technical SEO/AI optimization
    SEO = "seo"               # Traditional SEO
    BRANDING = "branding"     # Brand-specific recommendations


class RecommendationPriority(str, Enum):
    """Priority level of recommendation."""
    P0 = "P0"  # Critical - do immediately
    P1 = "P1"  # Important - do soon
    P2 = "P2"  # Nice to have


class RecommendationEffort(str, Enum):
    """Effort level to implement."""
    LOW = "low"       # < 1 day
    MEDIUM = "medium" # 1-5 days
    HIGH = "high"     # > 5 days


class RecommendationStatus(str, Enum):
    """Implementation status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DISMISSED = "dismissed"


class Recommendation(Base):
    """
    Optimization recommendation for improving AI visibility.
    
    Generated based on tracking data, analysis results,
    and citation patterns.
    """
    __tablename__ = "recommendations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Target brand
    brand: Mapped[str] = mapped_column(String(255), index=True)
    brand_normalized: Mapped[str] = mapped_column(String(255), index=True)
    
    # Recommendation details
    category: Mapped[str] = mapped_column(String(20), index=True)
    priority: Mapped[str] = mapped_column(String(5), index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    
    # Action steps (JSON array of strings)
    action_steps_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Impact and effort
    expected_impact: Mapped[str] = mapped_column(String(255))
    effort: Mapped[str] = mapped_column(String(20), default=RecommendationEffort.MEDIUM.value)
    
    # Status tracking
    status: Mapped[str] = mapped_column(
        String(20), 
        default=RecommendationStatus.PENDING.value,
        index=True
    )
    
    # Data source (JSON with references to analysis data)
    data_source_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Metrics
    impact_score: Mapped[float] = mapped_column(Float, default=0.0, comment="0-100 impact score")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    __table_args__ = (
        Index("ix_recommendations_brand_status", "brand_normalized", "status"),
        Index("ix_recommendations_priority_status", "priority", "status"),
    )
    
    def __repr__(self) -> str:
        return f"<Recommendation(id={self.id}, brand={self.brand}, title={self.title[:30]}...)>"


class LlmsTxtResult(Base):
    """
    Generated llms.txt content for a website.
    
    Stores the generated content along with configuration
    for future regeneration.
    """
    __tablename__ = "llms_txt_results"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Target website
    url: Mapped[str] = mapped_column(String(2048))
    domain: Mapped[str] = mapped_column(String(255), index=True)
    site_name: Mapped[str] = mapped_column(String(255))
    
    # Generated content
    content: Mapped[str] = mapped_column(Text)
    
    # Configuration used (for regeneration)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sections_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    topics_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    contact_info: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Generation settings
    auto_generated: Mapped[bool] = mapped_column(default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    __table_args__ = (
        Index("ix_llms_txt_domain_created", "domain", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<LlmsTxtResult(id={self.id}, domain={self.domain})>"


class OptimizationStats(Base):
    """
    Daily optimization statistics.
    
    Tracks recommendation generation and completion rates.
    """
    __tablename__ = "optimization_stats"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Date for aggregation
    date: Mapped[datetime] = mapped_column(DateTime, index=True)
    
    # Recommendation counts
    recommendations_generated: Mapped[int] = mapped_column(Integer, default=0)
    recommendations_completed: Mapped[int] = mapped_column(Integer, default=0)
    recommendations_dismissed: Mapped[int] = mapped_column(Integer, default=0)
    
    # llms.txt counts
    llms_txt_generated: Mapped[int] = mapped_column(Integer, default=0)
    
    # Impact tracking
    avg_impact_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<OptimizationStats(date={self.date}, generated={self.recommendations_generated})>"
