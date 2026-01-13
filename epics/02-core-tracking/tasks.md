# Tasks: 核心追踪系统

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 10 |
| Completed | 0 |
| In Progress | 0 |
| Remaining | 10 |
| Progress | 0% |

---

## Phase 1: 数据模型设计

**Goal**: 设计数据存储结构
**Status**: TODO

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 1.1 | 设计 Conversation 数据模型 | TODO | 2h | - | - | 存储对话数据 |
| 1.2 | 设计 BrandMention 数据模型 | TODO | 2h | - | - | 品牌提及记录 |
| 1.3 | 设计 VisibilityScore 数据模型 | TODO | 2h | - | - | 可见度分数 |

**Phase 1 Notes**:
- 使用 SQLAlchemy ORM
- 考虑索引优化查询性能

---

## Phase 2: API 开发

**Goal**: 实现数据接收和查询 API
**Status**: TODO
**Depends on**: Phase 1

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 2.1 | 实现数据上传 API | TODO | 2h | - | - | POST /api/tracking/upload |
| 2.2 | 实现可见度查询 API | TODO | 2h | - | - | GET /api/tracking/visibility |
| 2.3 | 实现排名查询 API | TODO | 2h | - | - | GET /api/tracking/ranking |
| 2.4 | 实现趋势数据 API | TODO | 2h | - | - | GET /api/tracking/trend |

**Phase 2 Notes**:
- 所有 API 使用 Pydantic schema 验证
- 添加分页支持

---

## Phase 3: 可见度计算

**Goal**: 实现可见度和排名计算逻辑
**Status**: TODO
**Depends on**: Phase 2

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 3.1 | 实现品牌识别服务 | TODO | 4h | - | - | 使用 Claude API |
| 3.2 | 实现可见度分数计算 | TODO | 3h | - | - | 公式实现 |
| 3.3 | 实现排名计算 | TODO | 2h | - | - | 竞品对比排名 |

**Phase 3 Notes**:
- 品牌识别可以异步处理
- 分数计算考虑多个维度

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
