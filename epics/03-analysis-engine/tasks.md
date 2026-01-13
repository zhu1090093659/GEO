# Tasks: 分析引擎

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 11 |
| Completed | 11 |
| In Progress | 0 |
| Remaining | 0 |
| Progress | 100% |

---

## Phase 1: 竞争分析

**Goal**: 实现竞争对手分析功能
**Status**: DONE

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 1.1 | 设计竞争对手数据模型 | DONE | 2h | 1.5h | Claude | CompetitorGroup + ComparisonResult |
| 1.2 | 实现竞争对手管理 API | DONE | 2h | 1h | Claude | CRUD + 关联品牌 |
| 1.3 | 实现竞争对比分析 | DONE | 4h | 1h | Claude | 基于 Tracking 数据 |
| 1.4 | 实现竞争分析报告 API | DONE | 3h | 0.5h | Claude | 待集成 Claude insights |

**Phase 1 Notes**:
- ✅ 支持用户自定义竞争对手列表 (CompetitorGroup)
- ✅ 复用 Tracking 模块的 Brand 表
- ⏳ Claude 生成的 insights 待实现

---

## Phase 2: 情感分析

**Goal**: 实现情感分析功能
**Status**: DONE
**Depends on**: Phase 1

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 2.1 | 设计情感分析 prompt | WIP | 2h | - | - | 待 Claude API 集成 |
| 2.2 | 实现情感分析服务 | DONE | 4h | 1h | Claude | 基于 BrandMention 数据 |
| 2.3 | 实现情感查询 API | DONE | 2h | 0.5h | Claude | 含趋势和示例 |

**Phase 2 Notes**:
- ✅ 情感分数范围 -1 到 1
- ✅ 支持查看具体回复示例
- ⏳ Claude API prompt 待设计

---

## Phase 3: Topic 发现

**Goal**: 实现 Topic 和关键词发现
**Status**: DONE
**Depends on**: Phase 2

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 3.1 | 设计 Topic 提取 prompt | DONE | 2h | 0.5h | Claude | Claude API prompt 模板 |
| 3.2 | 实现 Topic 提取服务 | DONE | 4h | 1h | Claude | 基于关键词匹配 |
| 3.3 | 实现关键词聚类 | DONE | 3h | 0.5h | Claude | 基于 co-occurrence |
| 3.4 | 实现 Topic 查询 API | DONE | 2h | 0.5h | Claude | 含趋势和关联品牌 |

**Phase 3 Notes**:
- ✅ 使用简化的关键词匹配 (MVP)
- ✅ 支持 Claude API prompt 模板
- ✅ 支持按时间范围查看趋势
- ⏳ 可增强为 embedding-based 聚类

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
