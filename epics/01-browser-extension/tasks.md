# Tasks: 浏览器扩展与数据收集

## Overview

| Metric | Value |
|--------|-------|
| Total Tasks | 15 |
| Completed | 0 |
| In Progress | 0 |
| Remaining | 15 |
| Progress | 0% |

---

## Phase 1: 扩展基础架构

**Goal**: 搭建 Chrome 扩展项目结构和基础配置
**Status**: TODO

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 1.1 | 创建 extension 目录和 package.json | TODO | 1h | - | - | |
| 1.2 | 配置 TypeScript 和构建工具 | TODO | 2h | - | - | 使用 Vite 或 webpack |
| 1.3 | 创建 manifest.json (Manifest V3) | TODO | 1h | - | - | |
| 1.4 | 实现基础 popup UI | TODO | 2h | - | - | 显示状态和控制 |
| 1.5 | 实现 Service Worker 基础框架 | TODO | 2h | - | - | background.ts |

**Phase 1 Notes**:
- 优先使用 Manifest V3 以符合 Chrome 最新要求
- popup 使用简单 HTML + TypeScript，无需框架

---

## Phase 2: 内容脚本开发

**Goal**: 实现 ChatGPT 和 Claude 的对话拦截
**Status**: TODO
**Depends on**: Phase 1

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 2.1 | 分析 ChatGPT DOM 结构 | TODO | 2h | - | - | 确定选择器 |
| 2.2 | 实现 ChatGPT 内容脚本 | TODO | 4h | - | - | MutationObserver |
| 2.3 | 分析 Claude DOM 结构 | TODO | 2h | - | - | 确定选择器 |
| 2.4 | 实现 Claude 内容脚本 | TODO | 4h | - | - | MutationObserver |

**Phase 2 Notes**:
- 使用 MutationObserver 监听 DOM 变化
- 需要处理流式输出场景（AI 逐字回复）
- 建立选择器配置文件，便于快速更新

---

## Phase 3: 后端 API 对接

**Goal**: 实现数据上传和后端接收接口
**Status**: TODO
**Depends on**: Phase 2

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 3.1 | 设计数据上传 API schema | TODO | 1h | - | - | |
| 3.2 | 实现后端 tracking API | TODO | 3h | - | - | FastAPI 路由 |
| 3.3 | 实现扩展端 API 调用 | TODO | 2h | - | - | 批量上传 |

**Phase 3 Notes**:
- 使用批量上传减少请求次数
- 实现本地队列和重试机制

---

## Phase 4: 用户授权流程

**Goal**: 实现隐私保护和用户授权
**Status**: TODO
**Depends on**: Phase 3

| ID | Task | Status | Est. | Actual | Assignee | Notes |
|----|------|--------|------|--------|----------|-------|
| 4.1 | 实现数据脱敏工具 | TODO | 2h | - | - | 邮箱、电话等 |
| 4.2 | 实现首次授权弹窗 | TODO | 2h | - | - | 用户确认 |
| 4.3 | 实现数据预览功能 | TODO | 2h | - | - | 查看待上传数据 |

**Phase 4 Notes**:
- 遵循 GDPR 和隐私保护最佳实践
- 用户可随时撤销授权

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
