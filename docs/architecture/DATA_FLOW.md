# GEO Data Flow Architecture

## Overview

This document describes how data flows through the GEO platform, from initial collection through analysis and optimization recommendations.

---

## Primary Data Flows

### 1. Data Collection Flow

The primary flow from browser extension to database:

```mermaid
flowchart TB
    subgraph browser [User's Browser]
        AI[AI Platform]
        CS[Content Script]
        BG[Background Worker]
        Store[Local Storage]
    end
    
    subgraph backend [Backend API]
        Upload[/tracking/upload]
        Validate[Validation]
        Extract[Brand Extraction]
        Calculate[Score Calculation]
    end
    
    subgraph db [Database]
        Conv[(conversations)]
        Msg[(messages)]
        Brand[(brands)]
        Mention[(brand_mentions)]
        Score[(visibility_scores)]
    end
    
    AI -->|DOM observation| CS
    CS -->|Sanitized data| BG
    BG -->|Queue locally| Store
    Store -->|Batch upload| Upload
    Upload --> Validate
    Validate --> Extract
    Extract --> Calculate
    
    Calculate --> Conv
    Calculate --> Msg
    Calculate --> Mention
    Calculate --> Score
```

**Steps**:
1. User interacts with AI platform (ChatGPT/Claude)
2. Content script observes DOM changes, captures query and response
3. Data is sanitized (PII removed) in content script
4. Background worker queues data locally
5. Batch uploaded to backend API
6. Backend validates, extracts brands, calculates scores
7. Data stored in normalized tables

---

### 2. Analysis Processing Flow

```mermaid
flowchart TB
    subgraph input [Input Data]
        Conv[(conversations)]
        Mention[(brand_mentions)]
    end
    
    subgraph analysis [Analysis Engine]
        Competitor[Competitor Analysis]
        Sentiment[Sentiment Analysis]
        Topic[Topic Extraction]
    end
    
    subgraph output [Analysis Results]
        Comp[(comparison_results)]
        Sent[(sentiment_analyses)]
        Top[(topics)]
        Kw[(keywords)]
    end
    
    Conv --> Topic
    Mention --> Competitor
    Mention --> Sentiment
    
    Competitor --> Comp
    Sentiment --> Sent
    Topic --> Top
    Topic --> Kw
```

---

### 3. Citation Extraction Flow

```mermaid
flowchart TB
    subgraph input [Input Sources]
        Msg[(messages)]
        Manual[Manual Text Input]
    end
    
    subgraph extract [Citation Extraction]
        URLParser[URL Parser]
        DomainParser[Domain Parser]
        NamedParser[Named Source Parser]
    end
    
    subgraph enrich [Enrichment]
        Authority[Authority Score]
        Aggregate[Source Aggregation]
    end
    
    subgraph output [Output]
        Cit[(citations)]
        Src[(citation_sources)]
    end
    
    Msg --> URLParser
    Msg --> DomainParser
    Msg --> NamedParser
    Manual --> URLParser
    
    URLParser --> Authority
    DomainParser --> Authority
    NamedParser --> Authority
    
    Authority --> Cit
    Authority --> Aggregate
    Aggregate --> Src
```

**Citation Types Detected**:

| Type | Pattern | Example |
|------|---------|---------|
| URL | `https?://...` | `https://example.com/page` |
| Domain | `according to X.com` | `According to salesforce.com` |
| Named | `according to X` | `According to Wikipedia` |

---

### 4. Optimization Recommendation Flow

```mermaid
flowchart TB
    subgraph inputs [Analysis Inputs]
        Vis[(visibility_scores)]
        Sent[(sentiment_analyses)]
        Cit[(citations)]
        Comp[(comparison_results)]
    end
    
    subgraph engine [Recommendation Engine]
        Template[8 Recommendation Templates]
        Evaluate[Data Evaluation]
        Score[Impact Scoring]
        Generate[Generate Recommendations]
    end
    
    subgraph output [Output]
        Rec[(recommendations)]
        Llms[(llms_txt_results)]
    end
    
    Vis --> Evaluate
    Sent --> Evaluate
    Cit --> Evaluate
    Comp --> Evaluate
    
    Evaluate --> Template
    Template --> Score
    Score --> Generate
    Generate --> Rec
    Generate --> Llms
```

**Recommendation Categories**:

| Category | Triggers |
|----------|----------|
| content | Low visibility, few mentions |
| structure | Poor citation rate |
| technical | Missing structured data |
| seo | Low search optimization |
| branding | Inconsistent brand mentions |

---

## Data Transformation Pipeline

### Input Transformation

```mermaid
flowchart LR
    Raw[Raw HTTP Request] --> Schema[Pydantic Schema]
    Schema -->|Invalid| Error[ValidationError 422]
    Schema -->|Valid| Service[Service Layer]
    Service --> Model[Domain Model]
    Model --> DB[(Database)]
```

### Output Transformation

```mermaid
flowchart LR
    DB[(Database)] --> Query[SQLAlchemy Query]
    Query --> Model[ORM Model]
    Model --> Schema[Response Schema]
    Schema --> JSON[JSON Response]
```

---

## Data Models

### Conversation Data Model

```mermaid
erDiagram
    conversations ||--o{ messages : contains
    conversations ||--o{ brand_mentions : has
    messages ||--o{ brand_mentions : triggers
    brands ||--o{ brand_mentions : referenced_in
    brands ||--o{ visibility_scores : tracked_by
    
    conversations {
        string id PK
        string session_id
        string platform
        string initial_query
        datetime captured_at
    }
    
    messages {
        int id PK
        string conversation_id FK
        string role
        text content
        int sequence
    }
    
    brands {
        int id PK
        string name
        string category
        bool is_competitor
    }
    
    brand_mentions {
        int id PK
        int brand_id FK
        int message_id FK
        string mention_type
        float sentiment
    }
    
    visibility_scores {
        int id PK
        int brand_id FK
        date date
        float score
        int mention_count
    }
```

### Analysis Data Model

```mermaid
erDiagram
    competitor_groups ||--o{ brands : contains
    competitor_groups ||--o{ comparison_results : produces
    brands ||--o{ sentiment_analyses : analyzed_in
    topics ||--o{ keywords : contains
    
    competitor_groups {
        int id PK
        string name
        string category
    }
    
    comparison_results {
        int id PK
        int group_id FK
        json results
        datetime created_at
    }
    
    sentiment_analyses {
        int id PK
        int brand_id FK
        float score
        string label
    }
    
    topics {
        int id PK
        string name
        int query_count
    }
    
    keywords {
        int id PK
        int topic_id FK
        string word
        int count
    }
```

---

## API Request/Response Flow

### Typical API Request

```mermaid
flowchart TB
    Client[Client Request] --> Router
    
    subgraph Router [FastAPI Router]
        Valid[Request Validation]
        Deps[Dependencies]
    end
    
    Router --> Service
    
    subgraph Service [Service Layer]
        BL[Business Logic]
    end
    
    Service --> Repo
    
    subgraph Repo [Repository Layer]
        ORM[SQLAlchemy ORM]
    end
    
    Repo --> DB[(Database)]
    
    DB --> Repo
    Repo --> Service
    Service --> Router
    Router --> Response[JSON Response]
```

---

## Event Processing

### Batch Processing Events

| Event | Trigger | Action |
|-------|---------|--------|
| Upload received | POST /tracking/upload | Process conversations, extract mentions |
| Score calculation | POST /tracking/calculate-scores | Calculate daily visibility scores |
| Topic extraction | POST /analysis/topics/extract | Process conversations for topics |
| Recommendation generation | POST /optimization/recommendations | Generate recommendations from data |

### Background Jobs (Planned)

| Job | Schedule | Action |
|-----|----------|--------|
| Daily score calculation | 00:00 UTC | Calculate all brand scores |
| Topic extraction | 06:00 UTC | Extract topics from new conversations |
| Stale data cleanup | 00:00 UTC | Remove data older than retention |

---

## Caching Strategy

### Current (MVP)

No caching layer - direct database queries.

### Planned (v0.2+)

```mermaid
flowchart LR
    Request([Request]) --> L1[Route Cache]
    L1 -->|Miss| L2[Redis Cache]
    L2 -->|Miss| DB[(Database)]
    DB --> L2
    L2 --> L1
    L1 --> Response([Response])
```

**Cache Keys**:

| Pattern | TTL | Invalidation |
|---------|-----|--------------|
| `visibility:{brand}:{date}` | 1h | On new mentions |
| `ranking:{date}` | 1h | On score recalculation |
| `topics:all` | 6h | On extraction |

---

## Error Handling Flow

```mermaid
flowchart TB
    Ex[Exception Raised] --> Handler[Exception Handler]
    Handler --> Log[Log Error]
    Handler --> Mapper[Error Mapper]
    Mapper --> Status[Map to HTTP Status]
    Status --> Response[Error Response]
    Response --> Client([Return to Client])
```

### Error Response Format

```json
{
    "detail": "Human readable error message"
}
```

### HTTP Status Mapping

| Exception | HTTP Status |
|-----------|-------------|
| ValidationError | 422 |
| NotFoundError | 404 |
| ConflictError | 409 |
| AuthenticationError | 401 |
| InternalError | 500 |

---

## Data Retention

| Data Type | Retention | Reason |
|-----------|-----------|--------|
| Raw conversations | 30 days | Privacy, storage |
| Brand mentions | 90 days | Detailed analysis |
| Visibility scores | 1 year | Trend analysis |
| Aggregated stats | Indefinite | Historical reporting |

---

## External Data Flows

### Outbound (Backend → External)

| Destination | Purpose | Data Sent |
|-------------|---------|-----------|
| Claude API | Agent analysis | Prompts, context |

### Inbound (External → Backend)

| Source | Purpose | Data Received |
|--------|---------|---------------|
| Browser Extension | Data collection | Conversations |
| Frontend | User queries | API requests |
