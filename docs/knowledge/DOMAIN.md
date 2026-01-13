# Domain Knowledge

## Business Overview

### What We Do

GEO (Generative Engine Optimization) 平台帮助品牌了解和优化其在 AI 生成回复中的曝光度。通过浏览器扩展收集真实用户与 AI（如 ChatGPT、Claude）的交互数据，分析品牌可见度、情感倾向和竞争态势，并提供可操作的优化建议。

### Target Users

| User Type | Description | Primary Goals |
|-----------|-------------|---------------|
| 品牌营销人员 | 负责品牌推广和市场营销 | 提升品牌在 AI 回复中的曝光度 |
| SEO 专家 | 专注于搜索引擎和内容优化 | 将 SEO 策略扩展到 AI 引擎 |
| 内容创作者 | 创作网站内容和文档 | 使内容更容易被 AI 引用 |

---

## Core Domain Concepts

### Visibility (可见度)

**Definition**: 品牌或产品在 AI 回复中被提及的频率和显著程度。

**Properties**:
- visibility_score: 可见度分数 (0-100)
- mention_count: 被提及次数
- mention_type: 提及类型（直接/间接/对比）
- position: 在回复中的位置

**Business Rules**:
- 直接提及权重 > 间接提及
- 首次出现位置越靠前，权重越高
- 正面情感提及权重更高

**Lifecycle**:
```
Data Collected -> Brand Identified -> Score Calculated -> Stored -> Reported
```

---

### Brand Mention (品牌提及)

**Definition**: AI 回复中对特定品牌、产品或服务的引用。

**Types**:
| Type | Description | Weight |
|------|-------------|--------|
| Direct | 直接提到品牌名称 | 1.0 |
| Indirect | 通过产品或服务间接提及 | 0.7 |
| Comparison | 在对比场景中提及 | 0.8 |
| Negative | 负面语境中提及 | -0.3 |

---

### Competitor (竞争对手)

**Definition**: 在同一市场或领域与目标品牌竞争的其他品牌。

**Properties**:
- name: 竞争对手名称
- category: 所属行业分类
- visibility_score: 可见度分数
- relative_rank: 相对排名

---

### Citation (引文)

**Definition**: AI 回复中引用的外部来源或参考资料。

**Types**:
| Type | Description | Example |
|------|-------------|---------|
| URL | 完整网址 | https://example.com/article |
| Domain | 域名引用 | "According to example.com..." |
| Named | 命名来源 | "According to Wikipedia..." |
| Implicit | 隐含引用 | 明显来自某来源但未标注 |

**Authority Levels**:
| Level | Score Range | Examples |
|-------|-------------|----------|
| High | 80-100 | .gov, .edu, major news |
| Medium | 50-79 | Industry publications |
| Low | 0-49 | Blogs, social media |

---

### Sentiment (情感)

**Definition**: AI 回复中对品牌的情感倾向。

**Scale**:
| Score | Label | Description |
|-------|-------|-------------|
| 0.5 to 1.0 | Positive | 正面评价、推荐 |
| -0.5 to 0.5 | Neutral | 客观陈述 |
| -1.0 to -0.5 | Negative | 负面评价、批评 |

---

### Topic (话题)

**Definition**: 用户向 AI 提问的主题分类。

**Properties**:
- name: 话题名称
- query_count: 相关查询数量
- trend: 趋势（上升/稳定/下降）
- related_keywords: 相关关键词

---

### llms.txt

**Definition**: 一种标准化文件格式，帮助 AI 更好地理解和索引网站内容。

**Structure**:
```
# Site Name
> Brief description
## Sections
- [Section](/path): Description
```

**Purpose**:
- 为 AI 提供结构化的网站概览
- 指导 AI 优先索引的内容
- 提供联系信息和授权说明

---

## Business Processes

### Data Collection Flow

```
1. User installs browser extension
2. User browses AI platforms (ChatGPT, Claude)
3. Extension captures query and response
4. Data sanitized (PII removed)
5. Data uploaded to GEO backend
6. Brand mentions extracted
7. Visibility scores calculated
```

**Edge Cases**:
- 网络不可用：本地缓存，稍后上传
- 数据脱敏失败：丢弃该条数据
- 品牌识别不确定：人工审核队列

---

### Analysis Process

```
1. Aggregate conversation data by brand
2. Run sentiment analysis on mentions
3. Extract topics and keywords
4. Compare with competitors
5. Generate visibility report
6. Create optimization recommendations
```

---

## Business Rules

### Visibility Score Calculation

| Factor | Weight | Description |
|--------|--------|-------------|
| Mention Count | 40% | 被提及的总次数 |
| Position Score | 30% | 在回复中的位置权重 |
| Sentiment Score | 20% | 情感倾向加权 |
| Context Quality | 10% | 提及上下文的相关性 |

### Data Retention Rules

| Data Type | Retention | Reason |
|-----------|-----------|--------|
| Raw Conversations | 30 days | 隐私保护 |
| Aggregated Scores | 1 year | 趋势分析 |
| Brand Mentions | 90 days | 详细分析需要 |

---

## External Integrations

### AI Platform Integration

**Purpose**: Capture conversation data
**Platforms**: ChatGPT, Claude
**Method**: Browser extension DOM monitoring

**Key Considerations**:
- DOM 结构可能变化
- 需要处理流式输出
- 遵守平台使用条款

---

### Claude API Integration

**Purpose**: Analysis and recommendations
**Provider**: Anthropic
**Documentation**: https://docs.anthropic.com/

**Use Cases**:
- 品牌实体识别
- 情感分析
- 优化建议生成

---

## Industry Context

### GEO vs SEO

| Aspect | SEO | GEO |
|--------|-----|-----|
| Target | Search Engines | AI Assistants |
| Ranking Factors | Keywords, Links | Content Quality, Citations |
| Optimization | Meta tags, Schema | llms.txt, Clear Structure |
| Measurement | Search Rankings | AI Mentions |

### Regulations

| Regulation | Applies To | Requirements |
|------------|------------|--------------|
| GDPR | User data collection | Consent, data minimization |
| CCPA | California users | Disclosure, opt-out rights |

---

## Metrics and KPIs

### Business Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Visibility Score | Brand exposure in AI | Increase 10% monthly |
| Share of Voice | Relative to competitors | Top 3 in category |
| Sentiment Score | Average brand sentiment | > 0.5 |

### Technical Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Data Collection Rate | Conversations/day | > 1000 |
| Analysis Latency | Time to process | < 5 minutes |
| API Response Time | p95 latency | < 500ms |

---

## FAQs

### Q: What is GEO?

A: GEO (Generative Engine Optimization) is the practice of optimizing content and brand presence to improve visibility in AI-generated responses, similar to how SEO optimizes for search engines.

### Q: How is visibility score calculated?

A: Visibility score is a weighted combination of mention frequency, position in responses, sentiment, and context quality. Higher scores indicate better brand exposure in AI responses.

### Q: What is llms.txt?

A: llms.txt is a standardized file format (similar to robots.txt for search engines) that helps AI systems understand and index website content more effectively.

### Q: How does the browser extension protect privacy?

A: The extension sanitizes data before upload, removing personally identifiable information (PII) like emails and phone numbers. Users must explicitly consent to data collection and can pause or disable collection at any time.
