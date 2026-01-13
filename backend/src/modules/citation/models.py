"""
Citation Module - SQLAlchemy ORM Models

Database models for citation extraction, source tracking,
and website analysis.
"""
from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import (
    String, Text, Integer, Float, DateTime, ForeignKey,
    Index, Boolean, JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class CitationType(str, Enum):
    """Type of citation found in AI response."""
    URL = "url"           # Direct URL link
    DOMAIN = "domain"     # Domain reference (e.g., "according to example.com")
    NAMED = "named"       # Named source (e.g., "according to Wikipedia")
    IMPLICIT = "implicit" # Implied reference without explicit source


class SourceType(str, Enum):
    """Category of citation source."""
    WEBSITE = "website"     # General website
    NEWS = "news"           # News outlet
    ACADEMIC = "academic"   # Academic/research paper
    SOCIAL = "social"       # Social media
    GOV = "gov"             # Government website
    EDU = "edu"             # Educational institution
    DOCS = "docs"           # Documentation/technical
    ECOMMERCE = "ecommerce" # E-commerce platform
    UNKNOWN = "unknown"     # Unknown type


class AnalysisStatus(str, Enum):
    """Status of website analysis."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Citation(Base):
    """
    Individual citation extracted from an AI response.
    
    Links back to the conversation and message where
    the citation was found.
    """
    __tablename__ = "citations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Source conversation/message (nullable for standalone extraction)
    conversation_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("conversations.id", ondelete="CASCADE"), index=True, nullable=True
    )
    message_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True
    )
    
    # Citation details
    source_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    source_domain: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    source_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    citation_type: Mapped[str] = mapped_column(String(20), default=CitationType.URL.value)
    
    # Scoring and context
    authority_score: Mapped[float] = mapped_column(Float, default=50.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.8, comment="Extraction confidence")
    context: Mapped[str] = mapped_column(Text, comment="Surrounding text context")
    position: Mapped[int] = mapped_column(Integer, default=0, comment="Position in response")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    conversation = relationship("Conversation", backref="citations")
    
    __table_args__ = (
        Index("ix_citations_domain_date", "source_domain", "created_at"),
        Index("ix_citations_type", "citation_type"),
    )
    
    def __repr__(self) -> str:
        return f"<Citation(id={self.id}, domain={self.source_domain}, type={self.citation_type})>"


class CitationSource(Base):
    """
    Aggregated source statistics.
    
    Tracks domains/sources that are frequently cited by AI,
    with authority scoring and metadata.
    """
    __tablename__ = "citation_sources"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Source identification
    domain: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    normalized_domain: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Classification
    source_type: Mapped[str] = mapped_column(String(20), default=SourceType.WEBSITE.value, index=True)
    
    # Metrics
    authority_score: Mapped[float] = mapped_column(Float, default=50.0)
    citation_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Metadata (title, description, logo URL, etc.)
    metadata_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Time tracking
    first_cited_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_cited_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Status
    is_verified: Mapped[bool] = mapped_column(default=False, comment="Manually verified source")
    is_active: Mapped[bool] = mapped_column(default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_citation_sources_type_count", "source_type", "citation_count"),
        Index("ix_citation_sources_authority", "authority_score"),
    )
    
    def __repr__(self) -> str:
        return f"<CitationSource(domain={self.domain}, count={self.citation_count})>"


class WebsiteAnalysis(Base):
    """
    Website analysis request and results.
    
    Stores both the analysis status and the final results,
    including recommendations for improving AI visibility.
    """
    __tablename__ = "website_analyses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Request details
    url: Mapped[str] = mapped_column(String(2048))
    domain: Mapped[str] = mapped_column(String(255), index=True)
    depth: Mapped[int] = mapped_column(Integer, default=1, comment="Pages analyzed")
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default=AnalysisStatus.PENDING.value, index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, comment="0-100 percent")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Results
    citation_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Citation contexts (JSON array of context objects)
    citation_contexts_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Recommendations (JSON array of recommendation objects)
    recommendations_json: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Analysis metadata
    pages_analyzed: Mapped[int] = mapped_column(Integer, default=0)
    content_length: Mapped[int] = mapped_column(Integer, default=0, comment="Total chars analyzed")
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Cache expiration")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_website_analyses_domain_status", "domain", "status"),
        Index("ix_website_analyses_created", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<WebsiteAnalysis(id={self.id}, domain={self.domain}, status={self.status})>"
