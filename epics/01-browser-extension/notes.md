# Notes: 浏览器扩展与数据收集

## Research Notes

### ChatGPT DOM 分析

待分析：
- 对话容器选择器
- 用户消息选择器
- AI 回复选择器
- 流式输出处理方式

### Claude DOM 分析

待分析：
- 对话容器选择器
- 用户消息选择器
- AI 回复选择器
- 流式输出处理方式

## Technical Decisions

### Manifest V3 vs V2

选择 V3：
- Chrome 强制要求新扩展使用 V3
- Service Worker 替代 background page
- 更好的安全性和性能

### 数据捕获方式

选择 DOM 监听（MutationObserver）：
- 比网络拦截更稳定
- 不需要处理复杂的 API 格式
- 可以捕获渲染后的完整内容

## Session Log

### 2026-01-13 - Session #2

**Completed**:
- [x] Phase 3: 后端 API 对接 (3.3 扩展端 API 调用)
- [x] Phase 4: 用户授权流程 (4.2 首次授权弹窗, 4.3 数据预览功能)
- [x] 全部 15 个任务完成，Epic 01 结束

**Notes**:
- asyncpg 在 Python 3.13 上编译失败，改用 aiosqlite (MVP 使用 SQLite)
- Windows PowerShell 不支持 `&&` 连接命令，需要分开执行
- Chrome 扩展需要从 `dist` 目录加载
- ChatGPT/Claude 的 DOM 选择器已配置化，方便后续维护

**Time Summary**:
- 预估总时间: 24h
- 实际总时间: ~15h
- 效率提升: 37%

**Next**:
- [ ] 手动测试扩展功能
- [ ] 开始 Epic 02 核心追踪系统

### 2026-01-13 - Session #1

**Completed**:
- [x] 项目初始化
- [x] 创建 5 个 Epic 目录结构
- [x] 更新核心文档

**Notes**:
- 项目从模板初始化成功

## Meeting Notes

(Add meeting notes here as the epic progresses)

## Links & Resources

- [Chrome Extension Manifest V3 Migration](https://developer.chrome.com/docs/extensions/migrating/mv2-to-mv3/)
- [MutationObserver API](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver)
