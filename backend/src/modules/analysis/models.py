"""
Analysis Module - SQLAlchemy ORM Models

Database models for competitor groups, analysis results,
sentiment analysis, and topic discovery.
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlalchemy import (
    String, Text, Integer, Float, DateTime, ForeignKey, 
    Index, Boolean, JSON, Table, Column
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class SentimentLabel(str, Enum):
    """Sentiment classification."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TrendDirection(str, Enum):
    """Trend direction indicator."""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


# Association table for CompetitorGroup <-> Brand many-to-many
competitor_group_brands = Table(
    "competitor_group_brands",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("competitor_groups.id", ondelete="CASCADE"), primary_key=True),
    Column("brand_id", Integer, ForeignKey("brands.id", ondelete="CASCADE"), primary_key=True),
)


class CompetitorGroup(Base):
    """
    Groups of competing brands for comparison analysis.
    
    Users can create groups like "CRM Software" or "E-commerce Platforms"
    to compare their brand against relevant competitors.
    """
    __tablename__ = "competitor_groups"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    
    # Owner brand (the brand being compared against competitors)
    owner_brand_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("brands.id", ondelete="SET NULL"), nullable=True
    )
    
    # Settings
    is_active: Mapped[bool] = mapped_column(default=True)
    auto_update: Mapped[bool] = mapped_column(default=True, comment="Auto-refresh analysis")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - use string reference to avoid circular import
    brands = relationship(
        "Brand",
        secondary=competitor_group_brands,
        backref="competitor_groups"
    )
    
    def __repr__(self) -> str:
        return f"<CompetitorGroup(id={self.id}, name={self.name})>"


class ComparisonResult(Base):
    """
    Cached results of competitor comparison analysis.
    
    Stores the results of comparing a brand against competitors
    to avoid re-computing expensive analysis.
    """
    __tablename__ = "comparison_results"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Comparison identifiers
    brand_normalized: Mapped[str] = mapped_column(String(255), index=True)
    competitor_normalized: Mapped[str] = mapped_column(String(255), index=True)
    group_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("competitor_groups.id", ondelete="CASCADE"), nullable=True
    )
    
    # Comparison metrics
    brand_visibility: Mapped[float] = mapped_column(Float, default=0.0)
    competitor_visibility: Mapped[float] = mapped_column(Float, default=0.0)
    visibility_diff: Mapped[float] = mapped_column(Float, default=0.0, comment="brand - competitor")
    
    brand_mentions: Mapped[int] = mapped_column(Integer, default=0)
    competitor_mentions: Mapped[int] = mapped_column(Integer, default=0)
    mention_diff: Mapped[int] = mapped_column(Integer, default=0)
    
    brand_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    competitor_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    sentiment_diff: Mapped[float] = mapped_column(Float, default=0.0)
    
    # AI-generated insights (from Claude)
    insights: Mapped[Optional[str]] = mapped_column(JSON, nullable=True, comment="Claude analysis insights")
    
    # Analysis metadata
    comparison_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime)
    period_end: Mapped[datetime] = mapped_column(DateTime)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_comparison_brands", "brand_normalized", "competitor_normalized"),
        Index("ix_comparison_date", "comparison_date"),
    )
    
    def __repr__(self) -> str:
        return f"<ComparisonResult(brand={self.brand_normalized} vs {self.competitor_normalized})>"


class SentimentAnalysis(Base):
    """
    Sentiment analysis results for brand mentions.
    
    Stores both individual mention sentiment and aggregated
    brand-level sentiment over time.
    """
    __tablename__ = "sentiment_analyses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Brand identification
    brand_normalized: Mapped[str] = mapped_column(String(255), index=True)
    
    # Analysis scope
    analysis_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    period_start: Mapped[datetime] = mapped_column(DateTime)
    period_end: Mapped[datetime] = mapped_column(DateTime)
    
    # Sentiment scores
    overall_sentiment: Mapped[float] = mapped_column(Float, comment="-1.0 to 1.0")
    sentiment_label: Mapped[str] = mapped_column(String(20))  # positive, neutral, negative
    
    # Distribution percentages
    positive_pct: Mapped[float] = mapped_column(Float, default=0.0)
    neutral_pct: Mapped[float] = mapped_column(Float, default=0.0)
    negative_pct: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Sample data (JSON)
    positive_samples: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    negative_samples: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Metadata
    mentions_analyzed: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_sentiment_brand_date", "brand_normalized", "analysis_date"),
    )
    
    def __repr__(self) -> str:
        return f"<SentimentAnalysis(brand={self.brand_normalized}, sentiment={self.overall_sentiment})>"


class Topic(Base):
    """
    Discovered topics from user queries.
    
    Topics are clusters of related queries that help understand
    what users are asking AI about.
    """
    __tablename__ = "topics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metrics
    query_count: Mapped[int] = mapped_column(Integer, default=0)
    mention_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Keywords (JSON array)
    keywords: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Trend
    trend: Mapped[str] = mapped_column(String(20), default="stable")
    growth_rate: Mapped[float] = mapped_column(Float, default=0.0, comment="% change")
    
    # Time tracking
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Related brands (JSON array of brand names)
    related_brands: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Topic(id={self.id}, name={self.name})>"


class Keyword(Base):
    """
    Trending keywords extracted from queries.
    
    Individual keywords that appear frequently in user queries,
    useful for understanding search patterns.
    """
    __tablename__ = "keywords"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    word: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    normalized_word: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    # Metrics
    count: Mapped[int] = mapped_column(Integer, default=0)
    query_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Trend
    trend: Mapped[str] = mapped_column(String(20), default="stable")
    growth_rate: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Related data (JSON)
    related_topics: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    related_brands: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    
    # Time tracking
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_keywords_count", "count"),
    )
    
    def __repr__(self) -> str:
        return f"<Keyword(word={self.word}, count={self.count})>"
