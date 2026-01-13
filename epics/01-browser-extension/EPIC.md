# Epic: 浏览器扩展与数据收集

## Overview

**ID**: 01
**Status**: DONE
**Priority**: P0
**Target Release**: v0.1
**Estimated Effort**: 5 days

---

## Goal

创建 Chrome 浏览器扩展，拦截用户与 AI 平台（ChatGPT、Claude）的对话，收集真实用户交互数据并上传至 GEO 后端。这是整个平台的数据来源基础，为后续的可见度追踪、竞争分析等功能提供原始数据支持。

---

## Success Criteria

- [x] Chrome 扩展可以成功安装并运行在 Chrome/Edge 浏览器
- [x] 能够拦截 ChatGPT (chat.openai.com) 的对话内容
- [x] 能够拦截 Claude (claude.ai) 的对话内容
- [x] 数据成功上传至后端 API 并存储
- [x] 用户隐私得到保护（数据脱敏、用户授权）

---

## User Stories

### Story 1: 安装扩展

**As a** 品牌营销人员
**I want to** 安装 GEO 浏览器扩展
**So that** 我可以开始收集 AI 交互数据

**Acceptance criteria**:
- [ ] 扩展可以从 Chrome Web Store 或本地安装
- [ ] 安装后显示欢迎页面和使用说明
- [ ] 扩展图标显示在浏览器工具栏

---

### Story 2: 自动捕获对话

**As a** 用户
**I want to** 扩展自动捕获我与 AI 的对话
**So that** 我不需要手动操作就能贡献数据

**Acceptance criteria**:
- [ ] 访问 ChatGPT 时自动开始捕获
- [ ] 访问 Claude 时自动开始捕获
- [ ] 捕获包含用户提问和 AI 回复
- [ ] 捕获包含时间戳和平台标识

---

### Story 3: 数据隐私控制

**As a** 注重隐私的用户
**I want to** 控制哪些数据被收集和上传
**So that** 我的敏感信息得到保护

**Acceptance criteria**:
- [ ] 可以暂停/恢复数据收集
- [ ] 可以查看待上传的数据
- [ ] 敏感信息（如邮箱、电话）被自动脱敏
- [ ] 首次使用时需要明确授权

---

## Technical Approach

### Architecture Impact

新增 Chrome 扩展项目，与后端 API 通信：

```
extension/
├── manifest.json         # Manifest V3 配置
├── src/
│   ├── background.ts     # Service Worker
│   ├── content/
│   │   ├── chatgpt.ts    # ChatGPT 内容脚本
│   │   └── claude.ts     # Claude 内容脚本
│   ├── popup/
│   │   ├── popup.html
│   │   └── popup.ts
│   └── utils/
│       ├── api.ts        # 后端 API 调用
│       └── sanitizer.ts  # 数据脱敏
├── package.json
└── tsconfig.json
```

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| 使用 Manifest V3 | Chrome 强制要求，更安全的 Service Worker 模式 |
| TypeScript 开发 | 类型安全，与前端项目一致 |
| DOM 监听方式捕获 | 比网络拦截更稳定，兼容性更好 |
| 批量上传策略 | 减少网络请求，提高效率 |

### Dependencies

- **Depends on**: 无（首个 Epic）
- **Depended by**: Epic 02 (核心追踪系统)

---

## Task Breakdown

See [tasks.md](./tasks.md) for detailed task list.

### Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: 扩展基础架构 | 5 tasks | DONE |
| Phase 2: 内容脚本开发 | 4 tasks | DONE |
| Phase 3: 后端 API 对接 | 3 tasks | DONE |
| Phase 4: 用户授权流程 | 3 tasks | DONE |

---

## Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| AI 平台 DOM 结构变化 | High | Medium | 抽象选择器，快速适配 |
| Chrome 扩展审核不通过 | Medium | High | 遵循政策，备用分发方式 |
| 用户隐私投诉 | Low | High | 完善授权机制，透明数据使用 |

---

## Open Questions

- [ ] 是否需要支持 Firefox 扩展？
  - Answer: MVP 阶段仅支持 Chrome，v0.2 考虑
- [ ] 数据存储期限？
  - Answer: 待定，建议 30 天滚动窗口

---

## References

- Chrome Extension Manifest V3: https://developer.chrome.com/docs/extensions/mv3/
- ChatGPT DOM 结构分析: TBD
- Claude DOM 结构分析: TBD

---

## Notes

- ChatGPT 和 Claude 的 DOM 结构可能随时变化，需要建立监控机制
- 考虑添加本地缓存，网络不可用时暂存数据
