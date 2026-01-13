# Epic: 引文系统

## Overview

**ID**: 04
**Status**: DONE
**Priority**: P1
**Target Release**: v0.1
**Estimated Effort**: 3 days
**Actual Effort**: 0.5 day

---

## Goal

构建引文发现和分析系统，识别 AI 回复中引用的来源和参考资料，并提供网站一键分析功能，帮助用户了解自己网站被 AI 引用的情况。

---

## Success Criteria

- [x] 能够从 AI 回复中提取引用的来源
- [x] 能够分析引用来源的权威性和相关性
- [x] 能够输入 URL 一键分析网站被 AI 引用情况
- [x] 提供引文来源的统计和趋势

---

## User Stories

### Story 1: 引文发现

**As a** 内容创作者
**I want to** 发现 AI 经常引用哪些来源
**So that** 我可以了解权威来源并学习

**Acceptance criteria**:
- [ ] 可以看到被引用最多的来源列表
- [ ] 可以看到引用来源的分类（官网/新闻/论文等）
- [ ] 可以查看具体的引用示例

---

### Story 2: 网站分析

**As a** 网站所有者
**I want to** 分析我的网站被 AI 引用的情况
**So that** 我可以优化内容以获得更多引用

**Acceptance criteria**:
- [ ] 输入 URL 后获取分析报告
- [ ] 可以看到网站被引用的次数和场景
- [ ] 可以获得内容优化建议

---

## Technical Approach

### Architecture Impact

新增 citation 模块到后端：

```
backend/src/modules/citation/
├── __init__.py
├── models.py           # 引文数据模型
├── schemas.py          # Pydantic schemas
├── service.py          # 引文服务
├── router.py           # API 路由
├── extractor.py        # 引文提取
└── analyzer.py         # 网站分析
```

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| 正则 + LLM 混合提取 | 正则处理明确格式，LLM 处理模糊引用 |
| 异步网站抓取 | 网站分析可能耗时 |

### Dependencies

- **Depends on**: Epic 02 (核心追踪系统)
- **Depended by**: Epic 05 (优化建议)

---

## Task Breakdown

See [tasks.md](./tasks.md) for detailed task list.

### Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: 引文提取 | 3 tasks | DONE |
| Phase 2: 网站分析 | 4 tasks | DONE |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 引文提取准确性 | Medium | Medium | 多种提取策略组合 |
| 网站抓取被阻止 | Low | Low | 使用标准 User-Agent |

---

## Open Questions

- [ ] 如何处理没有明确来源的引用？
  - Answer: 标记为"隐含引用"

---

## References

- URL 提取正则: TBD

---

## Notes

- 需要建立来源权威性评分体系
- 考虑缓存网站分析结果
