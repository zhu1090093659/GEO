# Tasks: 浏览器扩展与数据收集

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 15 |
| Completed | 15 |
| In Progress | 0 |
| Remaining | 0 |
| Progress | 100% |

---

## Phase 1: 扩展基础架构

**Goal**: 搭建 Chrome 扩展项目结构和基础配置
**Status**: DONE

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 1.1 | 创建 extension 目录和 package.json | DONE | 1h | 0.5h | Claude | 项目初始化时完成 |
| 1.2 | 配置 TypeScript 和构建工具 | DONE | 2h | 1h | Claude | 使用 Vite |
| 1.3 | 创建 manifest.json (Manifest V3) | DONE | 1h | 0.5h | Claude | |
| 1.4 | 实现基础 popup UI | DONE | 2h | 1h | Claude | HTML + TypeScript |
| 1.5 | 实现 Service Worker 基础框架 | DONE | 2h | 1h | Claude | background.ts |

**Phase 1 Notes**:
- ✅ 使用 Manifest V3 符合 Chrome 最新要求
- ✅ popup 使用简单 HTML + TypeScript
- ✅ 使用 Vite 构建，支持 watch 模式

---

## Phase 2: 内容脚本开发

**Goal**: 实现 ChatGPT 和 Claude 的对话拦截
**Status**: DONE
**Depends on**: Phase 1

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 2.1 | 分析 ChatGPT DOM 结构 | DONE | 2h | 1h | Claude | 选择器配置化 |
| 2.2 | 实现 ChatGPT 内容脚本 | DONE | 4h | 2h | Claude | MutationObserver + 去重 |
| 2.3 | 分析 Claude DOM 结构 | DONE | 2h | 1h | Claude | 选择器配置化 |
| 2.4 | 实现 Claude 内容脚本 | DONE | 4h | 2h | Claude | MutationObserver + 去重 |

**Phase 2 Notes**:
- ✅ 使用 MutationObserver 监听 DOM 变化
- ✅ 处理流式输出场景（防抖 + 完成检测）
- ✅ 建立选择器配置文件 (config/selectors.ts)
- ✅ 支持多级 fallback 选择器

---

## Phase 3: 后端 API 对接

**Goal**: 实现数据上传和后端接收接口
**Status**: DONE
**Depends on**: Phase 2

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 3.1 | 设计数据上传 API schema | DONE | 1h | 0.5h | Claude | 项目初始化时完成 |
| 3.2 | 实现后端 tracking API | DONE | 3h | 2h | Claude | FastAPI 路由已创建 |
| 3.3 | 实现扩展端 API 调用 | DONE | 2h | 1h | Claude | 端到端测试完成 |

**Phase 3 Notes**:
- ✅ 使用批量上传减少请求次数
- ✅ 实现本地队列和重试机制
- ✅ 后端端到端测试通过

---

## Phase 4: 用户授权流程

**Goal**: 实现隐私保护和用户授权
**Status**: DONE
**Depends on**: Phase 3

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 4.1 | 实现数据脱敏工具 | DONE | 2h | 1h | Claude | sanitizer.ts |
| 4.2 | 实现首次授权弹窗 | DONE | 2h | 1.5h | Claude | consent.html |
| 4.3 | 实现数据预览功能 | DONE | 2h | 1h | Claude | preview.html |

**Phase 4 Notes**:
- ✅ 数据脱敏已实现（邮箱、电话、信用卡、SSN、IP）
- ✅ 首次授权弹窗已实现（consent.html）
- ✅ 数据预览功能已实现（preview.html）

---

## Blocked Tasks

| Task ID | Blocked By | Expected Resolution |
|---------|------------|---------------------|
| - | - | - |

---

## Completed Tasks Log

| Task ID | Completed | Duration | Notes |
|---------|-----------|----------|-------|
| 1.1 | 2026-01-13 | 0.5h | 项目初始化时完成 |
| 1.2 | 2026-01-13 | 1h | Vite 配置 |
| 1.3 | 2026-01-13 | 0.5h | Manifest V3 |
| 1.4 | 2026-01-13 | 1h | popup UI |
| 1.5 | 2026-01-13 | 1h | Service Worker |
| 2.1 | 2026-01-13 | 1h | ChatGPT 选择器 |
| 2.2 | 2026-01-13 | 2h | ChatGPT 内容脚本 |
| 2.3 | 2026-01-13 | 1h | Claude 选择器 |
| 2.4 | 2026-01-13 | 2h | Claude 内容脚本 |
| 3.1 | 2026-01-13 | 0.5h | API Schema |
| 3.2 | 2026-01-13 | 2h | Tracking API |
| 4.1 | 2026-01-13 | 1h | 数据脱敏工具 |
| 4.2 | 2026-01-13 | 1.5h | 首次授权弹窗 |
| 4.3 | 2026-01-13 | 1h | 数据预览功能 |
| 3.3 | 2026-01-13 | 1h | 扩展端 API 调用 |

---

## Task Status Legend

| Status | Meaning |
|--------|---------|
| TODO | Not started |
| WIP | Work in progress |
| DONE | Completed and verified |
| BLOCKED | Waiting on dependency |
| SKIP | Decided not to do |

---

## Estimation Guidelines

| Estimate | Meaning |
|----------|---------|
| 1h | Trivial change, well understood |
| 2h | Small task, some complexity |
| 4h | Half day, moderate complexity |
| 8h | Full day, significant work |
| 16h+ | Consider breaking down further |

---

## Notes

- ChatGPT 和 Claude 的 DOM 选择器可能需要频繁更新
- 考虑建立自动化测试验证拦截功能
