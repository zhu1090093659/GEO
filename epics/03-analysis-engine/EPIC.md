# Epic: 分析引擎

## Overview

**ID**: 03
**Status**: TODO
**Priority**: P0
**Target Release**: v0.1
**Estimated Effort**: 5 days

---

## Goal

构建分析引擎模块，提供竞争对手分析、情感分析和 Topic/关键词发现功能。利用 Claude API 对收集的数据进行深度分析，帮助用户了解竞争态势和市场趋势。

---

## Success Criteria

- [ ] 能够分析竞争对手的可见度和表现
- [ ] 能够分析品牌在 AI 回复中的情感倾向
- [ ] 能够自动发现热门 Topic 和关键词
- [ ] 提供多语言和多区域分析支持

---

## User Stories

### Story 1: 竞争对手分析

**As a** 品牌营销人员
**I want to** 分析竞争对手在 AI 回复中的表现
**So that** 我可以制定竞争策略

**Acceptance criteria**:
- [ ] 可以添加竞争对手品牌
- [ ] 可以对比可见度分数
- [ ] 可以看到竞争对手的提及场景

---

### Story 2: 情感分析

**As a** 品牌营销人员
**I want to** 了解 AI 对我品牌的情感倾向
**So that** 我可以识别并改善负面认知

**Acceptance criteria**:
- [ ] 可以看到情感分数（正面/中性/负面）
- [ ] 可以看到情感趋势变化
- [ ] 可以查看具体的正面/负面回复示例

---

### Story 3: Topic 发现

**As a** 内容创作者
**I want to** 发现用户询问 AI 的热门话题
**So that** 我可以创作相关内容

**Acceptance criteria**:
- [ ] 可以看到热门 Topic 列表
- [ ] 可以看到 Topic 的搜索量趋势
- [ ] 可以发现与品牌相关的关键词

---

## Technical Approach

### Architecture Impact

新增 analysis 模块到后端：

```
backend/src/modules/analysis/
├── __init__.py
├── models.py           # 分析结果模型
├── schemas.py          # Pydantic schemas
├── service.py          # 分析服务
├── router.py           # API 路由
├── competitor.py       # 竞争分析
├── sentiment.py        # 情感分析
└── topic.py            # Topic 发现
```

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| 使用 Claude API 进行分析 | 利用现有 Agent 架构，高质量分析 |
| 批量分析 + 缓存 | 减少 API 调用成本 |
| 异步处理 | 分析任务可能耗时较长 |

### Dependencies

- **Depends on**: Epic 02 (核心追踪系统)
- **Depended by**: Epic 05 (优化建议)

---

## Task Breakdown

See [tasks.md](./tasks.md) for detailed task list.

### Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: 竞争分析 | 4 tasks | TODO |
| Phase 2: 情感分析 | 3 tasks | TODO |
| Phase 3: Topic 发现 | 4 tasks | TODO |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Claude API 成本高 | Medium | Medium | 批量处理，结果缓存 |
| 分析准确性 | Medium | High | 人工校验，持续优化 prompt |

---

## Open Questions

- [ ] 情感分析粒度？
  - Answer: 句子级别，聚合到品牌级别

---

## References

- Claude API Prompt Engineering: https://docs.anthropic.com/

---

## Notes

- 考虑使用 prompt 模板管理分析提示词
- 分析结果需要定期更新
