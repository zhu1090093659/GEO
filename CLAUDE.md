# Agent Project: GEO

> Solo Agent Agile Template - Build AI Agents powered by Claude Code

## Quick Context

GEO（生成式引擎优化）平台，通过浏览器扩展收集真实用户 AI 交互数据，提供品牌在 AI 回复中的可见度追踪、竞争分析和优化建议，帮助品牌营销人员、SEO 专家优化其在 AI 生成内容中的曝光度。

**Architecture**: React Frontend → FastAPI Backend → Claude Code CLI → Claude API + Chrome Extension

## Key Files

| Need | Location |
|------|----------|
| Agent System Prompt | @backend/src/modules/agent/prompts/system.md |
| Agent Service | @backend/src/modules/agent/service.py |
| Claude Code Driver | @backend/src/modules/agent/driver.py |
| Chat API Routes | @backend/src/modules/chat/router.py |
| Chat UI Components | @frontend/src/components/chat/ |
| Tracking Module | @backend/src/modules/tracking/ |
| Analysis Module | @backend/src/modules/analysis/ |
| Citation Module | @backend/src/modules/citation/ |
| Optimization Module | @backend/src/modules/optimization/ |
| Browser Extension | @extension/ |
| Current Status | @STATUS.md |
| Roadmap | @ROADMAP.md |

## Commands

```bash
# Development
make install          # Install dependencies
make dev              # Start frontend + backend
make dev-frontend     # Frontend only (port 3000)
make dev-backend      # Backend only (port 8000)

# Claude Code (in project)
/project:context      # Load current work context
/project:next         # Get next task
/project:done "msg"   # Mark task complete
/project:prompt       # Work on agent prompts
```

## Project Structure

```
backend/
  src/
    modules/
      agent/                # 核心 Agent 模块
        driver.py           # Claude Code CLI 驱动
        service.py          # Agent 服务层
        prompts/
          system.md         # 系统提示词 (重要!)
      chat/
        router.py           # Chat API 路由
      tracking/             # 追踪模块
        service.py          # 可见度/排名追踪服务
        models.py           # 追踪数据模型
      analysis/             # 分析引擎模块
        service.py          # 竞争分析/情感/关键词服务
      citation/             # 引文模块
        service.py          # 引文发现与网站分析
      optimization/         # 优化建议模块
        service.py          # 优化建议 + llms.txt 生成

extension/                  # Chrome 浏览器扩展
  manifest.json
  src/
    background.ts           # 后台脚本
    content.ts              # 内容脚本
    popup/                  # 弹窗 UI

frontend/
  src/
    components/
      chat/                 # 聊天 UI 组件
    hooks/
      useChat.ts            # SSE 流式 hook
    pages/
      HomePage.tsx          # 仪表盘主页
```

## Current Focus

> Update this section frequently

**Epic**: 01 - 浏览器扩展与数据收集
**Task**: 项目初始化与配置
**Status**: In Progress

## Agent Configuration

### Changing Personality

Edit: `backend/src/modules/agent/prompts/system.md`

### Restricting Tools

In `backend/src/modules/agent/service.py`:
```python
agent_service.set_allowed_tools(["Read", "Write", "Bash"])
```

### Adding Personas

Create: `backend/src/modules/agent/prompts/persona_[name].md`

## API Quick Reference

```bash
# Send message (streaming)
curl -N -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Reload prompt
curl -X POST http://localhost:8000/api/chat/admin/reload-prompt

# Upload tracking data (from extension)
curl -X POST http://localhost:8000/api/tracking/upload \
  -H "Content-Type: application/json" \
  -d '{"query": "...", "response": "...", "platform": "chatgpt"}'

# Get visibility report
curl http://localhost:8000/api/analysis/visibility?brand=example

# Analyze website
curl -X POST http://localhost:8000/api/citation/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

## Gotchas

- Claude Code CLI must be installed: `npm install -g @anthropic-ai/claude-code`
- ANTHROPIC_API_KEY must be set in `.env`
- Each session creates a workspace in `AGENT_WORKSPACE_DIR`
- Browser extension requires Chrome developer mode for local testing

## Quick Start for New Session

```bash
# For EXISTING projects - load current context
/project:context

# See what to do next
/project:next
```
