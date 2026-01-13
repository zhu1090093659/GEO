"""
Tracking Module - SQLAlchemy ORM Models

Database models for storing conversation data, brand mentions,
and visibility scores collected from AI platforms.
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum

from sqlalchemy import (
    String, Text, Integer, Float, DateTime, ForeignKey, Index, Enum as SQLEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


class Platform(str, Enum):
    """Supported AI platforms."""
    CHATGPT = "chatgpt"
    CLAUDE = "claude"
    PERPLEXITY = "perplexity"
    GEMINI = "gemini"
    OTHER = "other"


class MessageRole(str, Enum):
    """Message role in conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MentionType(str, Enum):
    """Type of brand mention."""
    DIRECT = "direct"           # Brand explicitly named
    INDIRECT = "indirect"       # Referenced without name
    COMPARISON = "comparison"   # Mentioned in comparison
    RECOMMENDATION = "recommendation"  # Recommended by AI
    NEGATIVE = "negative"       # Mentioned negatively


class Conversation(Base):
    """
    Stores a complete conversation session from AI platform.
    
    One conversation contains multiple messages (user questions + AI responses).
    """
    __tablename__ = "conversations"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True, comment="Browser session identifier")
    platform: Mapped[str] = mapped_column(SQLEnum(Platform), index=True)
    
    # First user query (for quick search)
    initial_query: Mapped[str] = mapped_column(Text, comment="First user question")
    
    # Metadata
    language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Timestamps
    captured_at: Mapped[datetime] = mapped_column(DateTime, comment="When conversation was captured")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages: Mapped[List["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )
    brand_mentions: Mapped[List["BrandMention"]] = relationship(
        "BrandMention", back_populates="conversation", cascade="all, delete-orphan"
    )
    
    # Indexes for common queries
    __table_args__ = (
        Index("ix_conversations_platform_date", "platform", "captured_at"),
        Index("ix_conversations_session", "session_id", "captured_at"),
    )
    
    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, platform={self.platform})>"


class Message(Base):
    """
    Individual message within a conversation.
    
    Stores both user messages and AI responses separately
    for detailed analysis.
    """
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    
    role: Mapped[str] = mapped_column(SQLEnum(MessageRole))
    content: Mapped[str] = mapped_column(Text)
    sequence: Mapped[int] = mapped_column(Integer, comment="Order in conversation (0-indexed)")
    
    # For streaming responses - track when message was complete
    is_complete: Mapped[bool] = mapped_column(default=True)
    
    # Timestamps
    timestamp: Mapped[datetime] = mapped_column(DateTime, comment="When message was sent/received")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    brand_mentions: Mapped[List["BrandMention"]] = relationship(
        "BrandMention", back_populates="message", cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index("ix_messages_conversation_seq", "conversation_id", "sequence"),
    )
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role}, conv={self.conversation_id})>"


class BrandMention(Base):
    """
    Brand mention extracted from AI response.
    
    Links to both conversation and specific message where
    the brand was mentioned.
    """
    __tablename__ = "brand_mentions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.id", ondelete="CASCADE"), index=True
    )
    message_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("messages.id", ondelete="CASCADE"), index=True
    )
    
    # Brand identification
    brand_name: Mapped[str] = mapped_column(String(255), index=True)
    brand_normalized: Mapped[str] = mapped_column(
        String(255), index=True, comment="Normalized brand name for matching"
    )
    
    # Mention details
    mention_type: Mapped[str] = mapped_column(SQLEnum(MentionType))
    position: Mapped[int] = mapped_column(Integer, comment="Character position in response")
    context: Mapped[str] = mapped_column(Text, comment="Surrounding text (±100 chars)")
    
    # Analysis results
    sentiment: Mapped[float] = mapped_column(
        Float, default=0.0, comment="Sentiment score -1.0 to 1.0"
    )
    confidence: Mapped[float] = mapped_column(
        Float, default=1.0, comment="Detection confidence 0.0 to 1.0"
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="brand_mentions")
    message: Mapped["Message"] = relationship("Message", back_populates="brand_mentions")
    
    __table_args__ = (
        Index("ix_brand_mentions_brand_date", "brand_normalized", "created_at"),
        Index("ix_brand_mentions_type", "mention_type", "brand_normalized"),
    )
    
    def __repr__(self) -> str:
        return f"<BrandMention(id={self.id}, brand={self.brand_name}, type={self.mention_type})>"


class VisibilityScore(Base):
    """
    Aggregated visibility score for a brand.
    
    Calculated periodically (daily) from brand mentions.
    Used for trend analysis and ranking.
    """
    __tablename__ = "visibility_scores"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Brand identification
    brand_name: Mapped[str] = mapped_column(String(255), index=True)
    brand_normalized: Mapped[str] = mapped_column(String(255), index=True)
    
    # Time period
    date: Mapped[datetime] = mapped_column(DateTime, index=True, comment="Date of score")
    platform: Mapped[Optional[str]] = mapped_column(
        SQLEnum(Platform), nullable=True, comment="Platform filter, null = all"
    )
    
    # Score components
    score: Mapped[float] = mapped_column(Float, comment="Final visibility score 0-100")
    mention_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_position: Mapped[float] = mapped_column(Float, default=0.0, comment="Avg position in responses")
    avg_sentiment: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Score breakdown
    position_score: Mapped[float] = mapped_column(Float, default=0.0, comment="Score from position")
    frequency_score: Mapped[float] = mapped_column(Float, default=0.0, comment="Score from frequency")
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0, comment="Score from sentiment")
    
    # Metadata
    conversation_count: Mapped[int] = mapped_column(Integer, default=0, comment="Conversations analyzed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("ix_visibility_brand_date", "brand_normalized", "date"),
        Index("ix_visibility_date_score", "date", "score"),
    )
    
    def __repr__(self) -> str:
        return f"<VisibilityScore(brand={self.brand_name}, date={self.date}, score={self.score})>"


class Brand(Base):
    """
    Brand registry for tracking.
    
    Stores brand metadata and aliases for improved detection.
    """
    __tablename__ = "brands"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    
    # Brand metadata
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Aliases for detection (JSON array stored as text)
    aliases: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="JSON array of aliases")
    
    # Tracking status
    is_active: Mapped[bool] = mapped_column(default=True)
    is_competitor: Mapped[bool] = mapped_column(default=False, comment="Mark as competitor for comparison")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Brand(id={self.id}, name={self.name})>"
