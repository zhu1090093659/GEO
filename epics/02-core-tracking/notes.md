# Notes: 核心追踪系统

## Data Model Design

### Conversation Table

```sql
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    user_query TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    platform TEXT NOT NULL,  -- chatgpt, claude
    language TEXT,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### BrandMention Table

```sql
CREATE TABLE brand_mentions (
    id TEXT PRIMARY KEY,
    conversation_id TEXT REFERENCES conversations(id),
    brand_name TEXT NOT NULL,
    mention_type TEXT,  -- direct, indirect, comparison
    position INTEGER,   -- position in response
    sentiment REAL,     -- -1 to 1
    context TEXT,       -- surrounding text
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### VisibilityScore Table

```sql
CREATE TABLE visibility_scores (
    id TEXT PRIMARY KEY,
    brand_name TEXT NOT NULL,
    date DATE NOT NULL,
    score REAL NOT NULL,
    mention_count INTEGER,
    avg_position REAL,
    avg_sentiment REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Visibility Score Formula

```
Score = Σ (mention_weight × position_weight × sentiment_weight)

Where:
- mention_weight: 1.0 for direct, 0.5 for indirect
- position_weight: 1.0 for first position, decreasing for later
- sentiment_weight: 1.0 + sentiment_score (0 to 2 range)
```

## API Design

### POST /api/tracking/upload

Request:
```json
{
  "conversations": [
    {
      "query": "...",
      "response": "...",
      "platform": "chatgpt",
      "timestamp": "2026-01-13T10:00:00Z"
    }
  ]
}
```

### GET /api/tracking/visibility

Query params:
- brand: string (required)
- start_date: date
- end_date: date

Response:
```json
{
  "brand": "example",
  "current_score": 85.5,
  "trend": [
    {"date": "2026-01-01", "score": 80.0},
    {"date": "2026-01-02", "score": 82.0}
  ]
}
```

## Links & Resources

- SQLAlchemy ORM: https://docs.sqlalchemy.org/
- FastAPI Background Tasks: https://fastapi.tiangolo.com/tutorial/background-tasks/
