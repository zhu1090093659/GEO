# Product Roadmap

## Vision

帮助品牌了解和优化其在 AI 生成回复中的曝光度和排名，通过浏览器扩展收集真实用户 AI 交互数据，提供可见度追踪、竞争分析和优化建议。

## Target Users

- Primary: 品牌营销人员、SEO 专家 - 需要了解品牌在 AI 回复中的表现
- Secondary: 内容创作者 - 希望优化内容以获得更多 AI 引用

---

## Release Plan

### v0.1 - MVP (Target: 2026-02-28)

> Goal: 验证核心追踪和分析能力，收集首批用户数据

| # | Epic | Status | Priority | Est. | Notes |
|---|------|--------|----------|------|-------|
| 01 | [浏览器扩展与数据收集](./epics/01-browser-extension/EPIC.md) | TODO | P0 | 5d | Chrome 扩展拦截 AI 对话 |
| 02 | [核心追踪系统](./epics/02-core-tracking/EPIC.md) | TODO | P0 | 4d | 可见度、排名计算与存储 |
| 03 | [分析引擎](./epics/03-analysis-engine/EPIC.md) | TODO | P0 | 5d | 竞争分析、情感、关键词 |
| 04 | [引文系统](./epics/04-citation-system/EPIC.md) | TODO | P1 | 3d | 引文提取与网站分析 |
| 05 | [优化建议系统](./epics/05-optimization/EPIC.md) | TODO | P1 | 3d | Agent 优化建议 + llms.txt |

**MVP Success Criteria**:
- [ ] 浏览器扩展成功捕获 ChatGPT/Claude 对话数据
- [ ] 用户可以查看品牌可见度报告
- [ ] 竞争对手分析功能可用
- [ ] 能够生成基本的优化建议

---

### v0.2 - Beta (Target: 2026-04-30)

> Goal: 增强分析能力，添加告警和高级功能

| # | Epic | Status | Priority | Est. | Notes |
|---|------|--------|----------|------|-------|
| 06 | AI 爬虫分析 | TODO | P1 | 5d | 爬虫时间、频率、引用分析 |
| 07 | 转化率追踪 | TODO | P1 | 4d | 关联 AI 推荐与转化 |
| 08 | 变更告警系统 | TODO | P2 | 3d | 可见度/排名变化通知 |
| 09 | ChatGPT Shopping 追踪 | TODO | P2 | 3d | 购物推荐可见度 |

---

### v1.0 - Public Release (Target: 2026-06-30)

> Goal: 生产就绪，支持多用户和团队协作

| # | Epic | Status | Priority | Est. | Notes |
|---|------|--------|----------|------|-------|
| 10 | 用户认证与多租户 | TODO | P0 | 5d | 用户系统、团队管理 |
| 11 | 高级报告与导出 | TODO | P1 | 3d | PDF 报告、数据导出 |
| 12 | API 开放平台 | TODO | P2 | 4d | 第三方集成 API |

---

## Backlog (Unscheduled)

Ideas and features not yet scheduled:

- [ ] 支持更多 AI 平台（Perplexity、Gemini、Copilot）
- [ ] 移动端扩展（Safari、Firefox）
- [ ] 自动化优化建议执行
- [ ] 行业基准对比报告
- [ ] Slack/Teams 集成通知

---

## Non-Goals

Things we explicitly will NOT build (to maintain focus):

- 不构建独立的爬虫系统 - 依赖浏览器扩展收集真实数据
- 不支持 IE 浏览器 - 现代 Chrome/Edge 优先
- 不构建自有 AI 模型 - 使用 Claude API 进行分析
- 不做实时竞价优化 - 专注于内容优化建议

---

## Dependencies & Risks

### External Dependencies

| Dependency | Risk Level | Mitigation |
|------------|------------|------------|
| Claude API | Medium | 本地缓存分析结果，支持降级 |
| Chrome Extension API | Low | 遵循 Manifest V3 规范 |
| AI 平台 DOM 结构 | High | 抽象拦截层，快速适配变化 |

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AI 平台反爬措施 | Medium | High | 模拟真实用户行为，限制频率 |
| 数据隐私合规 | Medium | High | 数据脱敏，用户授权机制 |
| 扩展被 Chrome 下架 | Low | High | 遵循 Chrome 政策，备用分发渠道 |

---

## Status Legend

| Symbol | Meaning |
|--------|---------|
| TODO | Not started |
| WIP | Work in progress |
| DONE | Completed |
| BLOCKED | Waiting on dependency |
| P0 | Must have for this release |
| P1 | Should have |
| P2 | Nice to have |
