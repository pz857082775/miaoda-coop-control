# Page Agent 集成参考

本目录包含从 `page-agent` 项目集成的参考文档。

## 集成内容

- **MCP 服务器**: `@page-agent/mcp` - 让 AI Agent 控制浏览器
- **Chrome 扩展**: Page Agent Extension
- **核心库**: page-agent core

## 快速开始

### 1. 安装 Chrome 扩展
访问: https://chromewebstore.google.com/detail/page-agent-ext/akldabonmimlicnjlflnapfeklbfemhj

### 2. 配置 LLM
需要配置环境变量:
```bash
export LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export LLM_API_KEY="your-api-key"
export LLM_MODEL_NAME="qwen3.5-plus"
```

### 3. 使用方式
在 miaoda-coop-control 中使用 `/浏览器操作` 指令 + 自然语言描述任务。

## MCP 工具

| 工具 | 说明 |
|------|------|
| execute_task | 用自然语言执行浏览器任务 |
| get_status | 获取连接状态 |
| stop_task | 停止当前任务 |

## 文档

详细文档见: `../../page-agent/README.md`
