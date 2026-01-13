# Epic: 优化建议系统

## Overview

**ID**: 05
**Status**: TODO
**Priority**: P1
**Target Release**: v0.1
**Estimated Effort**: 3 days

---

## Goal

构建优化建议系统，基于分析结果生成内容优化建议，并提供 llms.txt 索引页生成功能，帮助用户提升在 AI 回复中的可见度。

---

## Success Criteria

- [ ] 能够基于分析数据生成个性化优化建议
- [ ] 能够生成 llms.txt 索引页文件
- [ ] 优化建议可操作且具体
- [ ] 提供优化效果追踪

---

## User Stories

### Story 1: 获取优化建议

**As a** 品牌营销人员
**I want to** 获取提升 AI 可见度的优化建议
**So that** 我可以改善品牌在 AI 回复中的表现

**Acceptance criteria**:
- [ ] 可以看到针对性的优化建议列表
- [ ] 建议按优先级排序
- [ ] 每条建议包含具体操作步骤
- [ ] 可以追踪建议执行后的效果

---

### Story 2: 生成 llms.txt

**As a** 网站所有者
**I want to** 生成 llms.txt 索引页
**So that** AI 可以更好地理解和引用我的网站内容

**Acceptance criteria**:
- [ ] 输入网站 URL 后自动生成 llms.txt
- [ ] 可以预览和编辑生成的内容
- [ ] 提供部署指南

---

## Technical Approach

### Architecture Impact

新增 optimization 模块到后端：

```
backend/src/modules/optimization/
├── __init__.py
├── models.py           # 建议数据模型
├── schemas.py          # Pydantic schemas
├── service.py          # 优化建议服务
├── router.py           # API 路由
├── advisor.py          # 建议生成 (使用 Agent)
└── llms_generator.py   # llms.txt 生成器
```

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| 使用 Agent 生成建议 | 利用现有架构，高质量建议 |
| 模板化 llms.txt 生成 | 标准化输出格式 |

### Dependencies

- **Depends on**: Epic 03 (分析引擎), Epic 04 (引文系统)
- **Depended by**: None (终端功能)

---

## Task Breakdown

See [tasks.md](./tasks.md) for detailed task list.

### Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: 优化建议 | 4 tasks | TODO |
| Phase 2: llms.txt 生成 | 3 tasks | TODO |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 建议质量不高 | Medium | High | 持续优化 Agent prompt |
| llms.txt 规范变化 | Low | Low | 关注规范更新 |

---

## Open Questions

- [ ] llms.txt 规范是否有官方标准？
  - Answer: 参考 https://llmstxt.org/

---

## References

- llms.txt Specification: https://llmstxt.org/
- Agent Prompt Engineering: TBD

---

## Notes

- 建议需要定期更新，随数据变化
- 考虑支持建议的 A/B 测试
