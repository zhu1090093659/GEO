# Notes: 优化建议系统

## Session Notes

### 2026-01-13 - Session #4 - Epic 05 COMPLETED - MVP v0.1 DONE! 🎉

**Completed**:
- [x] Recommendation + LlmsTxtResult + OptimizationStats SQLAlchemy 数据模型
- [x] Alembic 迁移成功 (3 张新表)
- [x] 8 条优化建议模板 (数据驱动条件)
- [x] 建议生成服务 (基于 Tracking 数据)
- [x] 建议查询/更新 API
- [x] llms.txt 生成器 (符合 llmstxt.org 规范)
- [x] Preview + Download 功能
- [x] 统计 API

**Key Technical Decisions**:
1. 使用模板化建议而非纯 Claude 生成 (MVP 简化)
2. 建议根据品牌数据条件触发
3. Impact Score 用于排序优先级
4. llms.txt 缓存 30 天

**API Endpoints Implemented**:
- `POST /api/optimization/recommendations` - 生成建议
- `GET /api/optimization/recommendations` - 查询建议
- `PATCH /api/optimization/recommendations/{id}` - 更新状态
- `POST /api/optimization/llms-txt` - 生成 llms.txt
- `GET /api/optimization/llms-txt/{id}/preview` - 预览
- `GET /api/optimization/llms-txt/{id}/download` - 下载
- `GET /api/optimization/stats` - 统计

**Recommendation Categories**:
1. **content**: FAQ, 产品描述, 权威内容
2. **structure**: Schema.org markup
3. **technical**: llms.txt, AI 爬虫优化
4. **seo**: 域名权威
5. **branding**: 品牌情感

**MVP v0.1 Summary**:
- 5 个 Epic 全部完成
- 16+ 数据库表
- 30+ API 端点
- 约 4 小时开发时间

---

## Optimization Advisor Prompt

```
You are a GEO (Generative Engine Optimization) expert. Based on the following analysis data, provide actionable optimization recommendations.

Brand: {brand}
Current Visibility Score: {score}
Competitor Analysis: {competitor_data}
Sentiment Analysis: {sentiment_data}
Citation Analysis: {citation_data}

Please provide:
1. Top 5 optimization recommendations
2. For each recommendation:
   - Category (content/structure/technical)
   - Priority (P0/P1/P2)
   - Specific action steps
   - Expected impact
   - Estimated effort

Output as JSON:
{
  "recommendations": [
    {
      "id": 1,
      "title": "...",
      "category": "content",
      "priority": "P0",
      "description": "...",
      "action_steps": ["..."],
      "expected_impact": "...",
      "effort": "low/medium/high"
    }
  ]
}
```

## llms.txt Format

Based on https://llmstxt.org/:

```
# {Site Name}

> {Brief description}

## About

{Detailed description of the site/organization}

## Main Sections

- [Section 1](/path1): Description
- [Section 2](/path2): Description

## Key Topics

- Topic 1
- Topic 2

## Contact

- Website: {url}
- Email: {email}
```

## API Design

### GET /api/optimization/recommendations

Query params:
- brand: string (required)

Response:
```json
{
  "brand": "example",
  "generated_at": "2026-01-13T10:00:00Z",
  "recommendations": [
    {
      "id": 1,
      "title": "Improve product page content",
      "category": "content",
      "priority": "P0",
      "description": "Add more detailed product descriptions...",
      "action_steps": [
        "Review current product descriptions",
        "Add key features and benefits",
        "Include comparison with alternatives"
      ],
      "expected_impact": "15-20% visibility improvement",
      "effort": "medium"
    }
  ]
}
```

### POST /api/optimization/llms-txt

Request:
```json
{
  "url": "https://example.com",
  "site_name": "Example Corp",
  "description": "...",
  "auto_generate": true
}
```

Response:
```json
{
  "content": "# Example Corp\n\n> ...",
  "preview_url": "/preview/llms-txt/abc123",
  "download_url": "/download/llms-txt/abc123"
}
```

## Recommendation Categories

| Category | Examples |
|----------|----------|
| Content | Improve descriptions, add FAQs, update outdated info |
| Structure | Add schema markup, improve navigation, create sitemap |
| Technical | Improve page speed, add llms.txt, fix broken links |

## Links & Resources

- llms.txt Specification: https://llmstxt.org/
- Schema.org Markup: https://schema.org/
