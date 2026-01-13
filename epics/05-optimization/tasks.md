# Tasks: 优化建议系统

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 7 |
| Completed | 7 |
| In Progress | 0 |
| Remaining | 0 |
| Progress | 100% |

---

## Phase 1: 优化建议

**Goal**: 实现优化建议生成功能
**Status**: DONE

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 1.1 | 设计建议数据模型 | DONE | 1h | 0.5h | Claude | Recommendation + OptimizationStats |
| 1.2 | 设计建议生成 Agent prompt | DONE | 3h | 0.5h | Claude | 8 条模板建议 |
| 1.3 | 实现建议生成服务 | DONE | 4h | 0.5h | Claude | 基于数据驱动生成 |
| 1.4 | 实现建议查询 API | DONE | 2h | 0.5h | Claude | POST/GET/PATCH |

**Phase 1 Notes**:
- ✅ 建议分类：content, structure, technical, seo, branding
- ✅ 建议优先级：P0/P1/P2
- ✅ Impact Score 排序

---

## Phase 2: llms.txt 生成

**Goal**: 实现 llms.txt 文件生成
**Status**: DONE
**Depends on**: Phase 1

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 2.1 | 研究 llms.txt 规范 | DONE | 1h | 0.2h | Claude | 参考 llmstxt.org |
| 2.2 | 实现 llms.txt 生成器 | DONE | 4h | 0.5h | Claude | 模板化生成 |
| 2.3 | 实现生成 API | DONE | 2h | 0.3h | Claude | POST/preview/download |

**Phase 2 Notes**:
- ✅ 支持自定义和自动生成两种模式
- ✅ 30 天缓存过期
- ✅ Preview + Download 功能

---

## Blocked Tasks

| Task ID | Blocked By | Expected Resolution |
|---------|------------|---------------------|
| - | - | - |

---

## Completed Tasks Log

| Task ID | Completed | Duration | Notes |
|---------|-----------|----------|-------|
| - | - | - | - |

---

## Task Status Legend

| Status | Meaning |
|--------|---------|
| TODO | Not started |
| WIP | Work in progress |
| DONE | Completed and verified |
| BLOCKED | Waiting on dependency |
| SKIP | Decided not to do |
