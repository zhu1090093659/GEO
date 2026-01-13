# Notes: 核心追踪系统

## Session Log

### 2026-01-13 - Session #3

**Completed**:
- [x] Phase 1: 数据模型设计 (Conversation, Message, BrandMention, VisibilityScore, Brand)
- [x] Phase 2: API 开发 (upload, visibility, ranking, stats, brands, calculate-scores, rankings)
- [x] Phase 3: 可见度计算 (多维度加权公式 + 趋势分析)
- [x] Alembic 迁移配置
- [x] 端到端测试通过

**Notes**:
- 使用 SQLAlchemy async + aiosqlite 实现异步数据库操作
- 需要安装 greenlet 库才能正常运行 SQLAlchemy async
- 可见度分数公式: frequency(40%) + position(30%) + sentiment(20%) + type(10%)
- 品牌识别目前使用关键词匹配，后续可升级为 Claude API NER

**Time Summary**:
- 预估总时间: 4 days (~32h)
- 实际总时间: ~7h
- 效率提升: 78%

**Next**:
- [ ] 开始 Epic 03 - 分析引擎
- [ ] 实现竞争分析服务
- [ ] 实现情感分析 (Claude API)

---

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

## Visibility Score Formula (Implemented)

```
score = frequency(40%) + position(30%) + sentiment(20%) + type(10%)

Where:
- frequency_score: log1p(mention_rate * 10) / log1p(10), capped at 1.0
- position_score: exp(-avg_position / 500), min 0.1
- sentiment_score: (avg_sentiment + 1) / 2, normalized to [0,1]
- type_score: weighted average based on mention type multipliers:
  - RECOMMENDATION: 1.5
  - DIRECT: 1.0
  - COMPARISON: 0.8
  - INDIRECT: 0.6
  - NEGATIVE: 0.3
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
