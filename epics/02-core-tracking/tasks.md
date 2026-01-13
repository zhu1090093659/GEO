# Tasks: 核心追踪系统

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 10 |
| Completed | 10 |
| In Progress | 0 |
| Remaining | 0 |
| Progress | 100% |

---

## Phase 1: 数据模型设计

**Goal**: 设计数据存储结构
**Status**: DONE

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 1.1 | 设计 Conversation 数据模型 | DONE | 2h | 1h | Claude | 含 Message 子表 |
| 1.2 | 设计 BrandMention 数据模型 | DONE | 2h | 0.5h | Claude | 关联 Conversation + Message |
| 1.3 | 设计 VisibilityScore 数据模型 | DONE | 2h | 0.5h | Claude | 含 Brand 注册表 |

**Phase 1 Notes**:
- ✅ 使用 SQLAlchemy ORM + async
- ✅ 添加复合索引优化查询性能
- ✅ Alembic 迁移已生成并运行
- ✅ SQLite 数据库已创建 (geo.db)

---

## Phase 2: API 开发

**Goal**: 实现数据接收和查询 API
**Status**: DONE
**Depends on**: Phase 1

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 2.1 | 实现数据上传 API | DONE | 2h | 1h | Claude | 含品牌提及自动检测 |
| 2.2 | 实现可见度查询 API | DONE | 2h | 0.5h | Claude | 支持日期/平台过滤 |
| 2.3 | 实现排名查询 API | DONE | 2h | 0.5h | Claude | 支持竞品对比 |
| 2.4 | 实现趋势数据 API | DONE | 2h | 0.5h | Claude | 集成到 visibility 响应 |

**Phase 2 Notes**:
- ✅ 所有 API 使用 Pydantic schema 验证
- ✅ 使用 SQLAlchemy async session
- ✅ 添加品牌注册/列表 API
- ✅ 端到端测试通过

---

## Phase 3: 可见度计算

**Goal**: 实现可见度和排名计算逻辑
**Status**: DONE
**Depends on**: Phase 2

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 3.1 | 实现品牌识别服务 | DONE | 4h | 1h | Claude | 关键词匹配 + 别名支持 |
| 3.2 | 实现可见度分数计算 | DONE | 3h | 1h | Claude | 多维度加权公式 |
| 3.3 | 实现排名计算 | DONE | 2h | 0.5h | Claude | 含趋势分析 |

**Phase 3 Notes**:
- ✅ 品牌识别使用关键词匹配（支持别名）
- ✅ 分数公式: frequency(40%) + position(30%) + sentiment(20%) + type(10%)
- ✅ 趋势计算对比前后时间段
- ⏳ 后续可集成 Claude API 做高级 NER

---

## Blocked Tasks

| Task ID | Blocked By | Expected Resolution |
|---------|------------|---------------------|
| - | - | - |

---

## Completed Tasks Log

| Task ID | Completed | Duration | Notes |
|---------|-----------|----------|-------|
| 1.1 | 2026-01-13 | 1h | Conversation + Message 模型 |
| 1.2 | 2026-01-13 | 0.5h | BrandMention 模型 |
| 1.3 | 2026-01-13 | 0.5h | VisibilityScore + Brand 模型 |
| 2.1 | 2026-01-13 | 1h | POST /api/tracking/upload |
| 2.2 | 2026-01-13 | 0.5h | GET /api/tracking/visibility |
| 2.3 | 2026-01-13 | 0.5h | GET /api/tracking/ranking |
| 2.4 | 2026-01-13 | 0.5h | 集成到 visibility 响应 |
| 3.1 | 2026-01-13 | 1h | 关键词匹配 + 别名 |
| 3.2 | 2026-01-13 | 1h | 多维度加权公式 |
| 3.3 | 2026-01-13 | 0.5h | 含趋势分析 |

---

## Task Status Legend

| Status | Meaning |
|--------|---------|
| TODO | Not started |
| WIP | Work in progress |
| DONE | Completed and verified |
| BLOCKED | Waiting on dependency |
| SKIP | Decided not to do |
