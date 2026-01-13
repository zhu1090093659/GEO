# Glossary

## Purpose

This glossary ensures consistent terminology across code, documentation, and communication. When naming variables, classes, database tables, or API endpoints, use these terms exactly as defined.

---

## Core Business Terms

| Term | Definition | Usage Notes |
|------|------------|-------------|
| GEO | Generative Engine Optimization - 优化品牌在 AI 生成回复中的可见度 | 项目名称，全大写 |
| Visibility | 品牌在 AI 回复中的曝光程度 | Not "exposure" or "presence" |
| Mention | AI 回复中对品牌的引用 | Not "reference" or "citation" |
| Citation | AI 回复中引用的外部来源 | Not "source" or "link" |
| Topic | 用户查询的主题分类 | Not "category" or "subject" |

---

## Entity Terms

### User-Related

| Term | Definition | Code Usage |
|------|------------|------------|
| User | 使用 GEO 平台的注册用户 | `User`, `user_id` |
| Contributor | 安装扩展并贡献数据的用户 | `Contributor`, `contributor_id` |

### Brand-Related

| Term | Definition | Code Usage |
|------|------------|------------|
| Brand | 被追踪的品牌实体 | `Brand`, `brand_id` |
| BrandMention | AI 回复中的品牌提及记录 | `BrandMention`, `mention_id` |
| Competitor | 竞争对手品牌 | `Competitor`, `competitor_id` |

### Data-Related

| Term | Definition | Code Usage |
|------|------------|------------|
| Conversation | 用户与 AI 的一次对话 | `Conversation`, `conversation_id` |
| Query | 用户向 AI 提出的问题 | `query`, `user_query` |
| Response | AI 生成的回复 | `response`, `ai_response` |

### Analysis-Related

| Term | Definition | Code Usage |
|------|------------|------------|
| VisibilityScore | 品牌可见度分数 | `VisibilityScore`, `visibility_score` |
| SentimentScore | 情感分析分数 | `SentimentScore`, `sentiment_score` |
| Citation | 引文记录 | `Citation`, `citation_id` |
| Recommendation | 优化建议 | `Recommendation`, `recommendation_id` |

---

## Status Values

### Mention Type

| Status | Meaning | Code Value |
|--------|---------|------------|
| direct | 直接提及品牌名 | `"direct"` |
| indirect | 间接提及（通过产品等） | `"indirect"` |
| comparison | 在对比中提及 | `"comparison"` |
| negative | 负面语境中提及 | `"negative"` |

### Sentiment Label

| Status | Meaning | Score Range |
|--------|---------|-------------|
| positive | 正面情感 | 0.5 to 1.0 |
| neutral | 中性情感 | -0.5 to 0.5 |
| negative | 负面情感 | -1.0 to -0.5 |

### Analysis Status

| Status | Meaning | Can Transition To |
|--------|---------|-------------------|
| pending | 等待分析 | processing, cancelled |
| processing | 分析中 | completed, failed |
| completed | 分析完成 | - |
| failed | 分析失败 | pending (retry) |

### Recommendation Priority

| Status | Meaning | Description |
|--------|---------|-------------|
| P0 | 最高优先级 | 必须立即执行 |
| P1 | 高优先级 | 应该尽快执行 |
| P2 | 中优先级 | 有时间时执行 |

---

## Technical Terms

| Term | Definition | Context |
|------|------------|---------|
| Extension | Chrome 浏览器扩展 | Data collection |
| Content Script | 扩展注入页面的脚本 | Extension architecture |
| Service Worker | 扩展后台服务 | Extension architecture |
| DOM | Document Object Model | Web page structure |
| MutationObserver | DOM 变化监听 API | Data capture |

---

## Platform Names

| Platform | Domain | Code Value |
|----------|--------|------------|
| ChatGPT | chat.openai.com | `"chatgpt"` |
| Claude | claude.ai | `"claude"` |

---

## Abbreviations

| Abbr | Full Form | Context |
|------|-----------|---------|
| GEO | Generative Engine Optimization | Domain |
| SEO | Search Engine Optimization | Related concept |
| LLM | Large Language Model | AI technology |
| NER | Named Entity Recognition | Analysis method |
| PII | Personally Identifiable Information | Privacy |
| API | Application Programming Interface | General |
| DOM | Document Object Model | Web |
| SSE | Server-Sent Events | Streaming |

---

## Naming Conventions

### In Code

| Context | Convention | Example |
|---------|------------|---------|
| Class names | PascalCase | `VisibilityService` |
| Function names | snake_case | `calculate_visibility_score` |
| Variables | snake_case | `brand_mention` |
| Constants | UPPER_SNAKE | `MAX_MENTIONS_PER_BATCH` |
| Database tables | snake_case, plural | `brand_mentions` |
| API endpoints | kebab-case | `/api/tracking/visibility-score` |

### In Documentation

| Context | Convention | Example |
|---------|------------|---------|
| Referring to code | backticks | `VisibilityService` |
| File paths | backticks | `backend/src/modules/tracking/` |
| Concepts | normal text | visibility score |

---

## Confusing Terms Clarification

### Mention vs Citation

- **Mention**: AI 回复中提到的品牌或产品
- **Citation**: AI 回复中引用的外部来源（URL、网站等）

### Visibility vs Ranking

- **Visibility**: 绝对可见度分数 (0-100)
- **Ranking**: 与竞争对手对比的相对排名

### Query vs Prompt

- **Query**: 用户向 AI 提出的问题（本项目使用）
- **Prompt**: AI 系统提示词（内部使用）

### Topic vs Keyword

- **Topic**: 高层次的主题分类
- **Keyword**: 具体的搜索/查询词

---

## Domain-Specific Jargon

| Term | Definition | Example |
|------|------------|---------|
| Share of Voice | 品牌在行业中的相对曝光占比 | "Brand A has 30% share of voice" |
| Sentiment Drift | 情感分数随时间的变化 | "Positive sentiment drift over Q4" |
| Citation Authority | 引用来源的权威性评分 | ".gov sources have high authority" |
| llms.txt | AI 索引优化文件格式 | Similar to robots.txt |

---

## Deprecated Terms

| Deprecated | Use Instead | Reason |
|------------|-------------|--------|
| exposure | visibility | 统一术语 |
| reference | mention (for brands) | 区分品牌提及和引文 |
| source | citation | 更准确 |

---

## Adding New Terms

When adding a new term:

1. Check if a similar term already exists
2. Define clearly with usage context
3. Add code examples if applicable
4. Update relevant documentation
5. Notify team of new terminology
