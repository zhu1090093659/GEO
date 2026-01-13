# Notes: 引文系统

## Session Notes

### 2026-01-13 - Session #4 - Epic 04 COMPLETED

**Completed**:
- [x] Citation + CitationSource + WebsiteAnalysis SQLAlchemy 数据模型
- [x] Alembic 迁移成功 (3 张新表)
- [x] 引文提取服务 (正则匹配 URL/域名/命名来源)
- [x] 来源分类 (website, news, academic, social, gov, edu, docs, ecommerce)
- [x] 权威分数计算 (based on domain type)
- [x] 引文发现 API (`GET /api/citation/discover`)
- [x] 引文提取 API (`POST /api/citation/extract`)
- [x] 网站分析 API (`POST /api/citation/analyze`)
- [x] 分析状态查询 API (`GET /api/citation/analyze/{id}`)
- [x] 统计 API (`GET /api/citation/stats`)
- [x] 优化建议生成 (5 类建议)

**Key Technical Decisions**:
1. Citation.conversation_id 设为 nullable，支持独立文本提取
2. 网站分析结果缓存 24 小时
3. 来源权威分数基于域名类型自动计算
4. 推荐策略基于引用数量和权威分数

**API Endpoints Implemented**:
- `GET /api/citation/discover` - 发现引文来源
- `POST /api/citation/extract` - 从文本提取引文
- `POST /api/citation/analyze` - 分析网站
- `GET /api/citation/analyze/{id}` - 查询分析状态
- `GET /api/citation/stats` - 引文统计

**Issues & Solutions**:
1. conversation_id NOT NULL 约束导致独立提取失败 → 改为 nullable

**Recommendation Categories**:
1. **technical**: llms.txt, Schema.org markup
2. **content**: 权威内容创建, FAQ 扩展
3. **seo**: 域名权威建设

---

## Citation Extraction Patterns

### URL Patterns

```python
URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'
DOMAIN_PATTERN = r'(?:according to |source: |from )([a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z]{2,})+)'
```

### Citation Types

1. **Explicit URL**: Direct URL in response
2. **Domain Reference**: "According to example.com..."
3. **Named Source**: "According to Wikipedia..."
4. **Implicit**: Content clearly from a source but not cited

## Source Authority Scoring

| Source Type | Base Score |
|-------------|------------|
| Official .gov/.edu | 90 |
| Major news outlets | 80 |
| Wikipedia | 75 |
| Industry publications | 70 |
| Blogs/Personal sites | 50 |
| Social media | 40 |

## Website Analysis API

### POST /api/citation/analyze

Request:
```json
{
  "url": "https://example.com",
  "depth": 1  // pages to analyze
}
```

Response:
```json
{
  "url": "https://example.com",
  "analysis_id": "abc123",
  "status": "processing",
  "estimated_time": 30
}
```

### GET /api/citation/analyze/{analysis_id}

Response:
```json
{
  "url": "https://example.com",
  "status": "completed",
  "results": {
    "citation_count": 15,
    "citation_contexts": [
      {
        "query": "best CRM software",
        "response_snippet": "...example.com recommends...",
        "sentiment": 0.8
      }
    ],
    "recommendations": [
      "Add more structured data markup",
      "Improve content on topic X"
    ]
  }
}
```

## Links & Resources

- URL Regex Patterns: https://mathiasbynens.be/demo/url-regex
- Web Scraping Best Practices: TBD
