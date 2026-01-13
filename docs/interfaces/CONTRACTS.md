# GEO Module Interface Contracts

## Overview

This document defines the public interfaces between GEO modules. All cross-module communication should go through these defined contracts to ensure loose coupling and maintainability.

---

## Contract Principles

1. **Stability**: Once published, interfaces should not break backward compatibility
2. **Explicit**: All inputs and outputs must be typed
3. **Documented**: Each method must have clear documentation
4. **Versioned**: Breaking changes require version bump

---

## Module Contracts

### TrackingService

**Location**: `backend/src/modules/tracking/service.py`

The tracking service handles conversation data, brand mentions, and visibility scores.

```python
class TrackingService:
    """Tracking module interface for conversation and visibility management."""
    
    async def upload_conversations(
        self,
        db: AsyncSession,
        conversations: List[ConversationUploadItem]
    ) -> UploadResponse:
        """
        Upload conversation data from browser extension.
        
        Args:
            db: Database session
            conversations: List of conversation items to upload
            
        Returns:
            UploadResponse with counts of processed items
        """
        ...
    
    async def get_visibility(
        self,
        db: AsyncSession,
        brand: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        platform: Optional[str] = None
    ) -> VisibilityResponse:
        """
        Get visibility data for a brand.
        
        Args:
            db: Database session
            brand: Brand name to query
            start_date: Optional start date filter
            end_date: Optional end date filter
            platform: Optional platform filter
            
        Returns:
            VisibilityResponse with score, trend, and mentions
        """
        ...
    
    async def register_brand(
        self,
        db: AsyncSession,
        name: str,
        category: Optional[str] = None,
        description: Optional[str] = None,
        website: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        is_competitor: bool = False
    ) -> Brand:
        """
        Register a brand for tracking.
        
        Args:
            db: Database session
            name: Brand name (unique)
            category: Brand category
            description: Brand description
            website: Brand website URL
            aliases: Alternative names for the brand
            is_competitor: Whether this is a competitor brand
            
        Returns:
            Created Brand model instance
            
        Raises:
            ConflictError: If brand name already exists
        """
        ...
```

---

### AnalysisService

**Location**: `backend/src/modules/analysis/service.py`

The analysis service handles competitor comparisons, sentiment analysis, and topic discovery.

```python
class AnalysisService:
    """Analysis module interface for competitive and sentiment analysis."""
    
    async def compare_competitors(
        self,
        db: AsyncSession,
        brand: str,
        competitor_names: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> CompetitorComparisonResponse:
        """
        Compare brand visibility against competitors.
        
        Args:
            db: Database session
            brand: Primary brand to analyze
            competitor_names: Optional list of competitor names
            start_date: Optional start date
            end_date: Optional end date
            
        Returns:
            CompetitorComparisonResponse with rankings and insights
        """
        ...
    
    async def analyze_sentiment(
        self,
        db: AsyncSession,
        brand: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> SentimentResponse:
        """
        Analyze sentiment for a brand in AI responses.
        
        Args:
            db: Database session
            brand: Brand name to analyze
            start_date: Optional start date
            end_date: Optional end date
            
        Returns:
            SentimentResponse with score, distribution, and samples
        """
        ...
    
    async def discover_topics(
        self,
        db: AsyncSession,
        brand: Optional[str] = None,
        limit: int = 20
    ) -> TopicDiscoveryResponse:
        """
        Discover trending topics and keywords.
        
        Args:
            db: Database session
            brand: Optional brand filter
            limit: Maximum topics to return
            
        Returns:
            TopicDiscoveryResponse with topics and keywords
        """
        ...
```

---

### CitationService

**Location**: `backend/src/modules/citation/service.py`

The citation service handles citation extraction and website analysis.

```python
class CitationService:
    """Citation module interface for citation discovery and analysis."""
    
    async def discover_citations(
        self,
        db: AsyncSession,
        brand: Optional[str] = None,
        source_type: Optional[str] = None,
        limit: int = 50,
        days: int = 30
    ) -> CitationDiscoveryResponse:
        """
        Discover citations from AI responses.
        
        Args:
            db: Database session
            brand: Optional brand filter
            source_type: Optional source type filter
            limit: Maximum results
            days: Period to analyze
            
        Returns:
            CitationDiscoveryResponse with sources and statistics
        """
        ...
    
    async def extract_citations_from_text(
        self,
        db: AsyncSession,
        text: str,
        conversation_id: Optional[str] = None,
        message_id: Optional[int] = None
    ) -> ExtractCitationsResponse:
        """
        Extract citations from provided text.
        
        Args:
            db: Database session
            text: Text to analyze
            conversation_id: Optional conversation reference
            message_id: Optional message reference
            
        Returns:
            ExtractCitationsResponse with found citations
        """
        ...
    
    async def analyze_website(
        self,
        db: AsyncSession,
        url: str,
        depth: int = 1,
        force_refresh: bool = False
    ) -> WebsiteAnalysisResponse:
        """
        Analyze website for AI citation presence.
        
        Args:
            db: Database session
            url: Website URL to analyze
            depth: Number of pages to analyze
            force_refresh: Bypass cache
            
        Returns:
            WebsiteAnalysisResponse with analysis results
        """
        ...
```

---

### OptimizationService

**Location**: `backend/src/modules/optimization/service.py`

The optimization service handles recommendations and llms.txt generation.

```python
class OptimizationService:
    """Optimization module interface for recommendations and llms.txt."""
    
    async def generate_recommendations(
        self,
        db: AsyncSession,
        brand: str,
        focus_areas: Optional[List[str]] = None,
        include_completed: bool = False
    ) -> RecommendationsResponse:
        """
        Generate optimization recommendations for a brand.
        
        Args:
            db: Database session
            brand: Brand name
            focus_areas: Optional category filters
            include_completed: Include completed recommendations
            
        Returns:
            RecommendationsResponse with recommendations list
        """
        ...
    
    async def generate_llms_txt(
        self,
        db: AsyncSession,
        url: str,
        site_name: str,
        description: Optional[str] = None,
        auto_generate: bool = True,
        sections: Optional[List[Dict[str, str]]] = None,
        topics: Optional[List[str]] = None,
        contact_email: Optional[str] = None
    ) -> LlmsTxtResponse:
        """
        Generate llms.txt content for a website.
        
        Args:
            db: Database session
            url: Website URL
            site_name: Site name
            description: Site description
            auto_generate: Auto-discover sections
            sections: Manual section definitions
            topics: Key topics
            contact_email: Contact email
            
        Returns:
            LlmsTxtResponse with generated content
        """
        ...
```

---

### AgentService

**Location**: `backend/src/modules/agent/service.py`

The agent service wraps Claude Code CLI for AI agent capabilities.

```python
class AgentService:
    """Agent service interface for Claude Code integration."""
    
    def __init__(self, system_prompt: Optional[str] = None):
        """
        Initialize agent service.
        
        Args:
            system_prompt: Optional custom system prompt
        """
        ...
    
    async def execute(
        self,
        message: str,
        session_id: Optional[str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute agent with message and stream results.
        
        Args:
            message: User message
            session_id: Optional session ID for continuity
            
        Yields:
            Dict events: text, tool_use, tool_result, done
        """
        ...
    
    def reload_prompt(self) -> None:
        """Reload system prompt from file."""
        ...
```

---

## Shared DTOs

Common data transfer objects used across modules.

**Location**: `backend/src/modules/*/schemas.py`

### Core Types

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class DateRangeParams(BaseModel):
    """Date range filter parameters."""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TrendItem(BaseModel):
    """Generic trend data point."""
    date: str
    value: float
    count: int
```

### Tracking DTOs

```python
class ConversationUploadItem(BaseModel):
    """Single conversation for upload."""
    id: str
    session_id: str
    platform: str  # chatgpt, claude
    messages: List[MessageUploadItem]
    captured_at: str
    metadata: Optional[dict] = None


class MessageUploadItem(BaseModel):
    """Single message in conversation."""
    role: str  # user, assistant
    content: str
    timestamp: Optional[str] = None


class VisibilityResponse(BaseModel):
    """Visibility query response."""
    brand: str
    current_score: float
    previous_score: Optional[float]
    change_percent: Optional[float]
    trend: List[VisibilityTrendItem]
    total_mentions: int
    avg_sentiment: float
    period_days: int
```

### Analysis DTOs

```python
class CompetitorItem(BaseModel):
    """Competitor in comparison."""
    name: str
    visibility_score: float
    mention_count: int
    rank: int
    sentiment: float
    trend: str  # up, down, stable


class SentimentDistribution(BaseModel):
    """Sentiment breakdown."""
    positive: float  # 0-100
    neutral: float
    negative: float
```

---

## Error Contracts

Standard error types used across modules.

```python
from fastapi import HTTPException


class NotFoundError(HTTPException):
    """Resource not found - 404."""
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)


class ValidationError(HTTPException):
    """Invalid input - 400."""
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class ConflictError(HTTPException):
    """Resource conflict - 409."""
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)
```

### Error Response Format

```json
{
    "detail": "Human readable error message"
}
```

---

## Cross-Module Dependencies

### Dependency Matrix

| Module | Depends On |
|--------|------------|
| tracking | config, database |
| analysis | config, database, tracking |
| citation | config, database, tracking |
| optimization | config, database, analysis, citation |
| agent | config |
| chat | agent |

### Import Rules

```python
# Allowed: Import from lower-level modules
from src.modules.tracking.service import tracking_service
from src.modules.tracking.models import Brand, BrandMention

# Forbidden: Circular imports
# optimization cannot import from modules that import optimization
```

---

## Versioning Strategy

When making breaking changes:

1. Add deprecation warning to old interface
2. Create new version of interface
3. Support both versions during migration period
4. Remove old interface after migration

```python
import warnings

def old_method():
    warnings.warn(
        "old_method is deprecated, use new_method instead",
        DeprecationWarning
    )
    return new_method()
```

---

## Testing Contracts

Each module should have contract tests verifying:

1. Required methods exist
2. Method signatures match contract
3. Return types match contract
4. Errors raised match contract

```python
# tests/contracts/test_tracking_contract.py
async def test_tracking_service_upload_returns_upload_response():
    result = await tracking_service.upload_conversations(db, conversations)
    assert isinstance(result, UploadResponse)
    assert hasattr(result, 'received')
    assert hasattr(result, 'processed')
```
