# Notes: 分析引擎

## Session Notes

### 2026-01-13 - Session #4 - Epic 03 COMPLETED

**Completed**:
- [x] CompetitorGroup + ComparisonResult + SentimentAnalysis + Topic + Keyword 数据模型
- [x] Alembic 迁移成功 (6 张新表 + 索引)
- [x] 竞争对手组 CRUD API (create, list, get, add/remove competitor, delete)
- [x] 竞争对比分析服务 (基于 Tracking 数据实时计算)
- [x] 情感分析服务 (分布计算 + 趋势 + 示例)
- [x] Topic 提取服务 (关键词匹配 + 模式识别)
- [x] 关键词聚类服务 (co-occurrence 基础)
- [x] Claude prompt 模板 (sentiment.md, topic_extraction.md, competitor_insights.md)

**Key Technical Decisions**:
1. 复用 Tracking 模块的 Brand 表存储竞争对手，通过 `is_competitor` 字段区分
2. CompetitorGroup 与 Brand 多对多关系，使用 association table
3. 情感分析直接使用 BrandMention 中的 sentiment 字段（MVP 简化）
4. Topic 提取使用简化的关键词匹配，可后续升级为 Claude API

**API Endpoints Implemented**:
- `POST /api/analysis/competitor-groups` - 创建竞争对手组
- `GET /api/analysis/competitor-groups` - 列出所有组
- `GET /api/analysis/competitor-groups/{id}` - 获取单个组
- `POST /api/analysis/competitor-groups/{id}/competitors` - 添加竞争对手
- `DELETE /api/analysis/competitor-groups/{id}/competitors/{name}` - 移除竞争对手
- `DELETE /api/analysis/competitor-groups/{id}` - 删除组
- `GET /api/analysis/competitors/compare` - 竞争对比分析
- `GET /api/analysis/sentiment` - 情感分析
- `GET /api/analysis/topics` - Topic 发现
- `POST /api/analysis/topics/extract` - 触发 Topic 提取
- `POST /api/analysis/keywords/cluster` - 关键词聚类
- `GET /api/analysis/stats` - 统计数据

**Issues & Solutions**:
1. SQLAlchemy async 多对多关系懒加载问题 → 直接操作 association table
2. Alembic 迁移文件被删除后版本不一致 → 手动修复 alembic_version 表

**Prompts Created**:
- `prompts/sentiment.md` - 品牌情感分析
- `prompts/topic_extraction.md` - Topic 和关键词提取
- `prompts/competitor_insights.md` - 竞争分析洞察

---

## Sentiment Analysis Prompt

```
Analyze the sentiment towards the brand "{brand}" in the following AI response.

Response:
{response}

Please provide:
1. Overall sentiment score (-1 to 1, where -1 is very negative, 0 is neutral, 1 is very positive)
2. Sentiment label (positive/neutral/negative)
3. Key phrases that indicate the sentiment
4. Brief explanation

Output as JSON:
{
  "score": 0.5,
  "label": "positive",
  "key_phrases": ["reliable", "recommended"],
  "explanation": "..."
}
```

## Topic Extraction Prompt

```
Analyze the following user queries to AI assistants and extract the main topics and keywords.

Queries:
{queries}

Please identify:
1. Main topics (categories)
2. Trending keywords
3. User intent patterns

Output as JSON:
{
  "topics": [
    {"name": "product comparison", "count": 15, "keywords": ["best", "vs", "compare"]}
  ],
  "keywords": [
    {"word": "best", "count": 20, "trend": "rising"}
  ]
}
```

## Competitor Analysis Logic

1. Identify competitors from user input or industry defaults
2. Query visibility scores for all competitors
3. Calculate relative rankings
4. Identify differentiating factors
5. Generate comparison report

## API Design

### GET /api/analysis/competitors

Query params:
- brand: string (required)
- competitors: string[] (optional, comma-separated)

Response:
```json
{
  "brand": "example",
  "competitors": [
    {
      "name": "competitor1",
      "visibility_score": 75.0,
      "mention_count": 100,
      "rank": 2
    }
  ],
  "brand_rank": 1,
  "brand_score": 85.0
}
```

### GET /api/analysis/sentiment

Query params:
- brand: string (required)
- start_date: date
- end_date: date

Response:
```json
{
  "brand": "example",
  "overall_sentiment": 0.65,
  "sentiment_distribution": {
    "positive": 60,
    "neutral": 30,
    "negative": 10
  },
  "trend": [...]
}
```

## Links & Resources

- Sentiment Analysis Best Practices: TBD
- Topic Modeling with LLMs: TBD
