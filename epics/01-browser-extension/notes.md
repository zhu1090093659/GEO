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

## Meeting Notes

(Add meeting notes here as the epic progresses)

## Links & Resources

- [Chrome Extension Manifest V3 Migration](https://developer.chrome.com/docs/extensions/migrating/mv2-to-mv3/)
- [MutationObserver API](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver)
