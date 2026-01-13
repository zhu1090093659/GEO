# Epic: 核心追踪系统

## Overview

**ID**: 02
**Status**: TODO
**Priority**: P0
**Target Release**: v0.1
**Estimated Effort**: 4 days

---

## Goal

构建核心追踪系统，处理从浏览器扩展收集的数据，计算品牌在 AI 回复中的可见度和排名，并提供数据存储和查询能力。这是 GEO 平台的核心数据处理层。

---

## Success Criteria

- [ ] 能够接收并存储扩展上传的对话数据
- [ ] 能够识别 AI 回复中提及的品牌/产品
- [ ] 能够计算品牌可见度分数
- [ ] 能够计算品牌排名（与竞品对比）
- [ ] 提供 API 查询可见度和排名数据

---

## User Stories

### Story 1: 查看品牌可见度

**As a** 品牌营销人员
**I want to** 查看我的品牌在 AI 回复中的可见度
**So that** 我可以了解品牌的 AI 曝光情况

**Acceptance criteria**:
- [ ] 可以看到品牌被提及的次数
- [ ] 可以看到可见度趋势图
- [ ] 可以按时间范围筛选

---

### Story 2: 查看品牌排名

**As a** 品牌营销人员
**I want to** 查看我的品牌相对于竞争对手的排名
**So that** 我可以了解竞争态势

**Acceptance criteria**:
- [ ] 可以看到品牌在同类产品中的排名
- [ ] 可以添加竞争对手进行对比
- [ ] 排名基于可见度分数计算

---

## Technical Approach

### Architecture Impact

新增 tracking 模块到后端：

```
backend/src/modules/tracking/
├── __init__.py
├── models.py           # 数据模型
├── schemas.py          # Pydantic schemas
├── service.py          # 业务逻辑
├── router.py           # API 路由
└── calculator.py       # 可见度/排名计算
```

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| SQLite 存储 (MVP) | 简化开发，快速迭代 |
| 异步处理数据 | 避免阻塞 API 响应 |
| 品牌识别用 NER | 使用 Claude API 进行实体识别 |

### Dependencies

- **Depends on**: Epic 01 (浏览器扩展)
- **Depended by**: Epic 03 (分析引擎), Epic 04 (引文系统)

---

## Task Breakdown

See [tasks.md](./tasks.md) for detailed task list.

### Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: 数据模型设计 | 3 tasks | TODO |
| Phase 2: API 开发 | 4 tasks | TODO |
| Phase 3: 可见度计算 | 3 tasks | TODO |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| 品牌识别准确性 | Medium | High | 使用 Claude API + 人工校验 |
| 数据量增长快 | Medium | Medium | 设计分区策略，定期归档 |

---

## Open Questions

- [ ] 可见度分数计算公式？
  - Answer: 待定，初步考虑 (提及次数 × 位置权重 × 情感权重)

---

## References

- Named Entity Recognition with Claude: TBD

---

## Notes

- 需要建立品牌词库，支持品牌别名识别
- 考虑支持多语言品牌识别
