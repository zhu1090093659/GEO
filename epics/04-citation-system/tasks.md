# Tasks: 引文系统

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 7 |
| Completed | 7 |
| In Progress | 0 |
| Remaining | 0 |
| Progress | 100% |

---

## Phase 1: 引文提取

**Goal**: 实现引文发现和提取
**Status**: DONE

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 1.1 | 设计引文数据模型 | DONE | 2h | 1h | Claude | Citation, CitationSource, WebsiteAnalysis |
| 1.2 | 实现 URL/来源提取 | DONE | 4h | 1h | Claude | 正则匹配 URL/域名/命名来源 |
| 1.3 | 实现引文查询 API | DONE | 2h | 0.5h | Claude | discover, extract, stats |

**Phase 1 Notes**:
- ✅ 支持 URL、域名引用、命名来源三种类型
- ✅ 来源分类：website, news, academic, social, gov, edu, docs, ecommerce
- ✅ 自动计算权威分数 (based on domain type)

---

## Phase 2: 网站分析

**Goal**: 实现网站一键分析功能
**Status**: DONE
**Depends on**: Phase 1

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 2.1 | 设计网站分析 API | DONE | 1h | 0.5h | Claude | POST /analyze, GET /analyze/{id} |
| 2.2 | 实现网站内容抓取 | DONE | 3h | 0.5h | Claude | 简化版 (MVP) |
| 2.3 | 实现引用匹配分析 | DONE | 4h | 0.5h | Claude | 基于 citation 数据库查询 |
| 2.4 | 生成分析报告 | DONE | 2h | 0.5h | Claude | 5 类优化建议 |

**Phase 2 Notes**:
- ✅ 结果缓存 24 小时
- ✅ 自动生成 llms.txt、Schema.org、FAQ 等建议
- ⏳ 真实网页抓取待后续增强

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
