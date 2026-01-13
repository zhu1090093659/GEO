# GEO External API Reference

## Overview

Base URL: `http://localhost:8000/api`

The GEO API provides endpoints for brand visibility tracking, competitor analysis, citation discovery, and optimization recommendations in AI-generated content.

### API Documentation

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

## Common Response Format

### Success

```json
{
    "field1": "value",
    "field2": "value"
}
```

### Error

```json
{
    "detail": "Error message description"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

## Tracking API

Base path: `/tracking`

### POST /tracking/upload

Upload conversation data from browser extension.

**Request**:

```json
{
    "conversations": [
        {
            "id": "uuid-from-extension",
            "session_id": "browser-session-id",
            "platform": "chatgpt",
            "messages": [
                {
                    "role": "user",
                    "content": "What is the best CRM software?",
                    "timestamp": "2026-01-13T10:00:00Z"
                },
                {
                    "role": "assistant",
                    "content": "Based on your needs, I recommend Salesforce...",
                    "timestamp": "2026-01-13T10:00:05Z"
                }
            ],
            "captured_at": "2026-01-13T10:00:10Z",
            "metadata": {}
        }
    ]
}
```

**Response**: `200 OK`

```json
{
    "received": 1,
    "processed": 1,
    "brand_mentions_found": 3,
    "errors": []
}
```

---

### GET /tracking/visibility

Get visibility data for a brand.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | Yes | Brand name to query |
| start_date | datetime | No | Start date filter (ISO 8601) |
| end_date | datetime | No | End date filter (ISO 8601) |
| platform | string | No | Platform filter (chatgpt, claude) |

**Response**: `200 OK`

```json
{
    "brand": "Salesforce",
    "current_score": 75.5,
    "previous_score": 70.2,
    "change_percent": 7.5,
    "trend": [
        {
            "date": "2026-01-10",
            "score": 72.0,
            "mention_count": 15,
            "sentiment": 0.6
        }
    ],
    "total_mentions": 150,
    "avg_sentiment": 0.65,
    "period_days": 30
}
```

---

### GET /tracking/ranking

Get ranking data for a brand compared to competitors.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | Yes | Brand name to query |
| competitors | string | No | Comma-separated competitor names |
| start_date | datetime | No | Start date filter |
| end_date | datetime | No | End date filter |
| limit | int | No | Max results (default: 10, max: 50) |

**Response**: `200 OK`

```json
{
    "brand": "Salesforce",
    "brand_rank": 2,
    "brand_score": 75.5,
    "rankings": [
        {
            "brand_name": "HubSpot",
            "score": 80.2,
            "rank": 1,
            "mention_count": 200,
            "trend": "up",
            "change": 2
        },
        {
            "brand_name": "Salesforce",
            "score": 75.5,
            "rank": 2,
            "mention_count": 150,
            "trend": "stable",
            "change": 0
        }
    ],
    "total_brands": 10,
    "period": "2026-01-01 to 2026-01-13"
}
```

---

### GET /tracking/stats

Get overall tracking statistics.

**Response**: `200 OK`

```json
{
    "total_conversations": 5000,
    "total_messages": 15000,
    "total_brand_mentions": 3500,
    "total_brands_tracked": 50,
    "platforms": {
        "chatgpt": 3000,
        "claude": 2000
    },
    "date_range": {
        "earliest": "2026-01-01T00:00:00Z",
        "latest": "2026-01-13T23:59:59Z"
    }
}
```

---

### POST /tracking/brands

Register a brand for tracking.

**Request**:

```json
{
    "name": "Salesforce",
    "category": "CRM",
    "description": "Enterprise CRM platform",
    "website": "https://salesforce.com",
    "aliases": ["SFDC", "Salesforce CRM"],
    "is_competitor": false
}
```

**Response**: `200 OK`

```json
{
    "id": 1,
    "name": "Salesforce",
    "category": "CRM",
    "description": "Enterprise CRM platform",
    "website": "https://salesforce.com",
    "aliases": ["SFDC", "Salesforce CRM"],
    "is_competitor": false,
    "is_active": true,
    "created_at": "2026-01-13T10:00:00Z"
}
```

---

### GET /tracking/brands

List all registered brands.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| include_competitors | bool | No | Include competitor brands (default: true) |

**Response**: `200 OK`

```json
[
    {
        "id": 1,
        "name": "Salesforce",
        "category": "CRM",
        "description": "Enterprise CRM platform",
        "website": "https://salesforce.com",
        "aliases": ["SFDC"],
        "is_competitor": false,
        "is_active": true,
        "created_at": "2026-01-13T10:00:00Z"
    }
]
```

---

### POST /tracking/calculate-scores

Manually trigger visibility score calculation.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| date | datetime | No | Date to calculate scores for (default: today) |

**Response**: `200 OK`

```json
{
    "calculated": 10,
    "date": "2026-01-13",
    "scores": [
        {
            "brand": "Salesforce",
            "score": 75.5,
            "mentions": 50
        }
    ]
}
```

---

### GET /tracking/rankings

Get brand rankings based on visibility scores.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| start_date | datetime | No | Start date |
| end_date | datetime | No | End date |
| limit | int | No | Maximum brands (default: 20, max: 100) |

**Response**: `200 OK`

```json
{
    "rankings": [
        {
            "brand": "HubSpot",
            "score": 80.2,
            "rank": 1,
            "trend": "up"
        }
    ],
    "total": 10,
    "period": {
        "start": "2025-12-14",
        "end": "2026-01-13"
    }
}
```

---

## Analysis API

Base path: `/analysis`

### POST /analysis/competitor-groups

Create a new competitor group.

**Request**:

```json
{
    "name": "CRM Leaders",
    "description": "Top CRM platforms",
    "category": "CRM",
    "owner_brand": "Salesforce",
    "competitor_names": ["HubSpot", "Zoho", "Pipedrive"]
}
```

**Response**: `200 OK`

```json
{
    "id": 1,
    "name": "CRM Leaders",
    "description": "Top CRM platforms",
    "category": "CRM",
    "owner_brand": null,
    "competitors": ["HubSpot", "Zoho", "Pipedrive"],
    "is_active": true,
    "created_at": "2026-01-13T10:00:00Z"
}
```

---

### GET /analysis/competitor-groups

List all competitor groups.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| category | string | No | Filter by category |

**Response**: `200 OK`

```json
[
    {
        "id": 1,
        "name": "CRM Leaders",
        "description": "Top CRM platforms",
        "category": "CRM",
        "owner_brand": null,
        "competitors": ["HubSpot", "Zoho", "Pipedrive"],
        "is_active": true,
        "created_at": "2026-01-13T10:00:00Z"
    }
]
```

---

### GET /analysis/competitor-groups/{group_id}

Get a specific competitor group by ID.

**Response**: `200 OK`

```json
{
    "id": 1,
    "name": "CRM Leaders",
    "description": "Top CRM platforms",
    "category": "CRM",
    "owner_brand": null,
    "competitors": ["HubSpot", "Zoho", "Pipedrive"],
    "is_active": true,
    "created_at": "2026-01-13T10:00:00Z"
}
```

**Errors**:
- `404` - Competitor group not found

---

### POST /analysis/competitor-groups/{group_id}/competitors

Add a competitor to an existing group.

**Request**:

```json
{
    "name": "Monday.com"
}
```

**Response**: `200 OK`

```json
{
    "success": true,
    "message": "Added Monday.com to group"
}
```

---

### DELETE /analysis/competitor-groups/{group_id}/competitors/{competitor_name}

Remove a competitor from a group.

**Response**: `200 OK`

```json
{
    "success": true,
    "message": "Removed Monday.com from group"
}
```

---

### DELETE /analysis/competitor-groups/{group_id}

Delete a competitor group.

**Response**: `200 OK`

```json
{
    "success": true,
    "message": "Competitor group deleted"
}
```

---

### GET /analysis/competitors/compare

Compare brand visibility against competitors.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | Yes | Brand name to compare |
| competitors | string | No | Comma-separated competitor names |
| start_date | datetime | No | Start date filter |
| end_date | datetime | No | End date filter |

**Response**: `200 OK`

```json
{
    "brand": "Salesforce",
    "brand_score": 75.5,
    "brand_rank": 2,
    "brand_mentions": 150,
    "brand_sentiment": 0.65,
    "competitors": [
        {
            "name": "HubSpot",
            "visibility_score": 80.2,
            "mention_count": 200,
            "rank": 1,
            "sentiment": 0.70,
            "trend": "up"
        }
    ],
    "insights": "Your brand is performing well but trails HubSpot...",
    "analysis_date": "2026-01-13T10:00:00Z",
    "period": "Last 30 days"
}
```

---

### GET /analysis/sentiment

Analyze sentiment for a brand in AI responses.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | Yes | Brand name to analyze |
| start_date | datetime | No | Start date filter |
| end_date | datetime | No | End date filter |

**Response**: `200 OK`

```json
{
    "brand": "Salesforce",
    "overall_sentiment": 0.65,
    "sentiment_label": "positive",
    "distribution": {
        "positive": 65.0,
        "neutral": 25.0,
        "negative": 10.0
    },
    "trend": [
        {
            "date": "2026-01-10",
            "sentiment": 0.60,
            "mention_count": 15
        }
    ],
    "samples": [
        {
            "query": "Best enterprise CRM?",
            "response_snippet": "Salesforce is often considered the gold standard...",
            "sentiment_score": 0.8,
            "sentiment_label": "positive",
            "platform": "chatgpt",
            "timestamp": "2026-01-13T10:00:00Z"
        }
    ],
    "mentions_analyzed": 150,
    "period_days": 30
}
```

---

### GET /analysis/topics

Discover trending topics and keywords.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | No | Optional brand filter |
| limit | int | No | Maximum topics (default: 20, max: 100) |

**Response**: `200 OK`

```json
{
    "topics": [
        {
            "id": 1,
            "name": "CRM comparison",
            "query_count": 500,
            "keywords": ["best CRM", "CRM features", "pricing"],
            "trend": "up",
            "growth_rate": 15.5,
            "related_brands": ["Salesforce", "HubSpot"]
        }
    ],
    "keywords": [
        {
            "word": "CRM",
            "count": 1000,
            "trend": "stable",
            "growth_rate": 2.0,
            "related_topics": ["CRM comparison"],
            "related_brands": ["Salesforce"]
        }
    ],
    "total_queries_analyzed": 5000,
    "analysis_period": "Last 30 days"
}
```

---

### POST /analysis/topics/extract

Extract topics and keywords from recent conversations.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| start_date | datetime | No | Start date filter |
| end_date | datetime | No | End date filter |

**Response**: `200 OK`

```json
{
    "success": true,
    "topics_extracted": 25,
    "keywords_extracted": 100,
    "conversations_processed": 500
}
```

---

### POST /analysis/keywords/cluster

Cluster keywords into related groups.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| min_count | int | No | Minimum keyword count (default: 5) |

**Response**: `200 OK`

```json
{
    "success": true,
    "clusters": 10,
    "keywords_clustered": 50
}
```

---

### GET /analysis/stats

Get overall analysis statistics.

**Response**: `200 OK`

```json
{
    "total_competitor_groups": 5,
    "total_comparisons": 100,
    "total_sentiment_analyses": 500,
    "total_topics": 25,
    "total_keywords": 200,
    "last_analysis_date": "2026-01-13T10:00:00Z"
}
```

---

## Citation API

Base path: `/citation`

### GET /citation/discover

Discover citations from collected AI responses.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | No | Optional brand filter |
| source_type | string | No | Filter by source type |
| limit | int | No | Maximum results (default: 50, max: 100) |
| days | int | No | Period in days (default: 30, max: 365) |

**Response**: `200 OK`

```json
{
    "total_citations": 500,
    "total_sources": 100,
    "sources": [
        {
            "id": 1,
            "domain": "salesforce.com",
            "display_name": "Salesforce",
            "source_type": "company",
            "authority_score": 85.0,
            "citation_count": 50,
            "avg_sentiment": 0.7,
            "first_cited_at": "2026-01-01T00:00:00Z",
            "last_cited_at": "2026-01-13T10:00:00Z",
            "is_verified": true
        }
    ],
    "top_domains": [
        {"domain": "salesforce.com", "count": 50}
    ],
    "by_type": {
        "url": 300,
        "domain": 150,
        "named": 50
    },
    "by_source_type": {
        "company": 200,
        "news": 150,
        "documentation": 100
    },
    "period": "Last 30 days"
}
```

---

### POST /citation/extract

Extract citations from provided text.

**Request**:

```json
{
    "text": "According to Salesforce's documentation at salesforce.com...",
    "conversation_id": "uuid-optional",
    "message_id": 123
}
```

**Response**: `200 OK`

```json
{
    "citations_found": 2,
    "citations": [
        {
            "id": 1,
            "source_url": "https://salesforce.com",
            "source_domain": "salesforce.com",
            "source_name": "Salesforce",
            "citation_type": "domain",
            "authority_score": 85.0,
            "confidence": 0.95,
            "context": "According to Salesforce's documentation...",
            "created_at": "2026-01-13T10:00:00Z"
        }
    ],
    "sources_updated": 1
}
```

---

### POST /citation/analyze

Analyze a website for AI citation presence.

**Request**:

```json
{
    "url": "https://example.com",
    "depth": 2,
    "force_refresh": false
}
```

**Response**: `200 OK`

```json
{
    "id": 1,
    "url": "https://example.com",
    "domain": "example.com",
    "status": "completed",
    "progress": 100,
    "citation_count": 25,
    "avg_sentiment": 0.6,
    "citation_contexts": [
        {
            "query": "What is example.com?",
            "response_snippet": "Example.com provides...",
            "sentiment": 0.7,
            "citation_type": "domain",
            "platform": "chatgpt",
            "timestamp": "2026-01-13T10:00:00Z"
        }
    ],
    "recommendations": [
        {
            "category": "content",
            "title": "Add structured data",
            "description": "Implement JSON-LD schema markup...",
            "priority": "P1",
            "impact": "high",
            "effort": "medium"
        }
    ],
    "pages_analyzed": 5,
    "started_at": "2026-01-13T10:00:00Z",
    "completed_at": "2026-01-13T10:05:00Z",
    "error_message": null
}
```

---

### GET /citation/analyze/{analysis_id}

Get status of website analysis.

**Response**: `200 OK`

```json
{
    "id": 1,
    "status": "completed",
    "progress": 100,
    "estimated_time_seconds": null,
    "result": { /* WebsiteAnalysisResponse */ }
}
```

---

### GET /citation/stats

Get overall citation statistics.

**Response**: `200 OK`

```json
{
    "total_citations": 5000,
    "total_sources": 500,
    "total_analyses": 50,
    "top_source_types": {
        "company": 2000,
        "news": 1500,
        "documentation": 1000
    },
    "top_citation_types": {
        "url": 3000,
        "domain": 1500,
        "named": 500
    },
    "avg_authority_score": 65.5,
    "recent_citations_count": 100
}
```

---

## Optimization API

Base path: `/optimization`

### POST /optimization/recommendations

Generate optimization recommendations for a brand.

**Request**:

```json
{
    "brand": "Salesforce",
    "focus_areas": ["content", "seo"],
    "include_completed": false
}
```

**Response**: `200 OK`

```json
{
    "brand": "Salesforce",
    "generated_at": "2026-01-13T10:00:00Z",
    "recommendations": [
        {
            "id": 1,
            "brand": "Salesforce",
            "category": "content",
            "priority": "P0",
            "title": "Create comprehensive product comparison pages",
            "description": "Develop detailed comparison content...",
            "action_steps": [
                "Identify top 5 competitors",
                "Create feature comparison matrix",
                "Add use case examples"
            ],
            "expected_impact": "high",
            "effort": "medium",
            "impact_score": 8.5,
            "status": "pending",
            "created_at": "2026-01-13T10:00:00Z",
            "updated_at": "2026-01-13T10:00:00Z",
            "completed_at": null
        }
    ],
    "summary": {
        "total": 8,
        "by_priority": {"P0": 2, "P1": 4, "P2": 2},
        "by_category": {"content": 3, "seo": 3, "technical": 2},
        "by_status": {"pending": 8},
        "avg_impact_score": 7.5
    },
    "new_count": 8
}
```

---

### GET /optimization/recommendations

Get existing recommendations for a brand.

**Query Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | Yes | Brand name |
| status | string | No | Filter by status (pending, in_progress, completed, dismissed) |
| category | string | No | Filter by category |

**Response**: `200 OK`

```json
[
    {
        "id": 1,
        "brand": "Salesforce",
        "category": "content",
        "priority": "P0",
        "title": "Create comprehensive product comparison pages",
        "description": "Develop detailed comparison content...",
        "action_steps": ["Step 1", "Step 2"],
        "expected_impact": "high",
        "effort": "medium",
        "impact_score": 8.5,
        "status": "pending",
        "created_at": "2026-01-13T10:00:00Z",
        "updated_at": "2026-01-13T10:00:00Z",
        "completed_at": null
    }
]
```

---

### PATCH /optimization/recommendations/{recommendation_id}

Update recommendation status.

**Request**:

```json
{
    "status": "completed",
    "notes": "Implemented comparison page for top 5 competitors"
}
```

**Response**: `200 OK`

```json
{
    "id": 1,
    "brand": "Salesforce",
    "category": "content",
    "priority": "P0",
    "title": "Create comprehensive product comparison pages",
    "description": "...",
    "action_steps": [],
    "expected_impact": "high",
    "effort": "medium",
    "impact_score": 8.5,
    "status": "completed",
    "created_at": "2026-01-13T10:00:00Z",
    "updated_at": "2026-01-13T12:00:00Z",
    "completed_at": "2026-01-13T12:00:00Z"
}
```

---

### POST /optimization/llms-txt

Generate llms.txt content for a website.

**Request**:

```json
{
    "url": "https://example.com",
    "site_name": "Example Company",
    "description": "Leading provider of example services",
    "auto_generate": true,
    "sections": [
        {
            "name": "Products",
            "path": "/products",
            "description": "Our product catalog"
        }
    ],
    "topics": ["examples", "tutorials"],
    "contact_email": "contact@example.com"
}
```

**Response**: `200 OK`

```json
{
    "id": 1,
    "url": "https://example.com",
    "domain": "example.com",
    "site_name": "Example Company",
    "content": "# Example Company\n\n> Leading provider of example services\n\n...",
    "sections": [
        {
            "name": "Products",
            "path": "/products",
            "description": "Our product catalog"
        }
    ],
    "preview_url": "/api/optimization/llms-txt/1/preview",
    "download_url": "/api/optimization/llms-txt/1/download",
    "created_at": "2026-01-13T10:00:00Z"
}
```

---

### GET /optimization/llms-txt/{result_id}/preview

Preview generated llms.txt content.

**Response**: `200 OK` (text/plain)

```
# Example Company

> Leading provider of example services

## Products
- [Product Catalog](/products): Our product catalog

## Contact
- Email: contact@example.com
```

---

### GET /optimization/llms-txt/{result_id}/download

Download generated llms.txt file.

**Response**: `200 OK` (text/plain with Content-Disposition header)

Returns file download with filename `llms.txt`.

---

### GET /optimization/stats

Get optimization module statistics.

**Response**: `200 OK`

```json
{
    "total_recommendations": 100,
    "recommendations_by_status": {
        "pending": 50,
        "in_progress": 20,
        "completed": 25,
        "dismissed": 5
    },
    "recommendations_by_category": {
        "content": 40,
        "seo": 30,
        "technical": 20,
        "structure": 10
    },
    "recommendations_by_priority": {
        "P0": 20,
        "P1": 50,
        "P2": 30
    },
    "total_llms_txt_generated": 25,
    "avg_impact_score": 7.2,
    "completion_rate": 25.0
}
```

---

## Chat API

Base path: `/chat`

### POST /chat/message

Send a message to the AI agent (SSE streaming).

**Request**:

```json
{
    "message": "Analyze visibility for brand XYZ",
    "session_id": "optional-session-id"
}
```

**Response**: Server-Sent Events stream

```
event: text
data: {"type": "text", "content": "I'll analyze..."}

event: tool_use
data: {"type": "tool_use", "tool": "Read", "input": {"file": "..."}}

event: tool_result
data: {"type": "tool_result", "tool": "Read", "output": "..."}

event: done
data: {"type": "done"}
```

---

### POST /chat/admin/reload-prompt

Reload the agent system prompt.

**Response**: `200 OK`

```json
{
    "status": "ok",
    "message": "Prompt reloaded"
}
```

---

## Extension Data Format

### Platform Values

| Platform | Value |
|----------|-------|
| ChatGPT | `chatgpt` |
| Claude | `claude` |

### Message Roles

| Role | Description |
|------|-------------|
| `user` | User's question/prompt |
| `assistant` | AI's response |

### Mention Types

| Type | Description | Weight |
|------|-------------|--------|
| `direct` | Brand name mentioned directly | 1.0 |
| `indirect` | Referenced via product/service | 0.7 |
| `comparison` | Mentioned in comparison context | 0.8 |
| `negative` | Mentioned negatively | -0.3 |

### Sentiment Labels

| Label | Score Range |
|-------|-------------|
| `positive` | 0.5 to 1.0 |
| `neutral` | -0.5 to 0.5 |
| `negative` | -1.0 to -0.5 |

### Recommendation Statuses

| Status | Description |
|--------|-------------|
| `pending` | Not yet started |
| `in_progress` | Currently being implemented |
| `completed` | Successfully implemented |
| `dismissed` | Marked as not applicable |

### Recommendation Priorities

| Priority | Description |
|----------|-------------|
| `P0` | Critical - implement immediately |
| `P1` | High - implement soon |
| `P2` | Medium - implement when possible |
