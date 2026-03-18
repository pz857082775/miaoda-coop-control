---
name: miaoda-coop-control
version: 0.2.0
description: |
  秒哒开发协作管控 - 自动化执行版。支持自动更新升级、浏览器自动化操作（基于Page Agent+OpenClaw Zero Token免API）。
  版权: 米乐 | 版本: 0.2.0
  触发条件：(1) /新建应用 (2) /优化 (3) /修复 (4) /检查更新 (5) /浏览器操作 (6) /安装扩展 (7) /配置AI
---

# 秒哒开发协作管控 v0.2.0

## 技能信息

| 项目 | 内容 |
|------|------|
| **技能名称** | 秒哒开发协作管控 |
| **版本** | 0.2.0 |
| **版权** | 米乐 |
| **平台** | OpenClaw |
| **GitHub** | pz857082775/miaoda-coop-control |

---

## 核心功能

### 1. 自动化任务调度
- 接收指令 → 解析 → 执行 → 反馈

### 2. 多AI模型支持（免API）
- 豆包、DeepSeek、KIMI、文心一言、千问、GPT、智谱
- **无需API Key** - 基于 OpenClaw Zero Token
- 通过网页登录方式免费使用各大AI平台

### 3. 需求队列缓存
- 繁忙时不拦截，自动收集合并

### 4. 应用管理
- 自动生成应用ID
- 状态跟踪管理

### 5. 自动更新检查
- 支持检查新版本
- 提醒用户更新

### 6. 浏览器自动化操作
- 基于阿里 Page Agent + OpenClaw Zero Token
- 自然语言控制网页
- 自动复制AI回复内容
- 自动化网页操作
- **免费使用AI大模型**

### 7. 自动安装Chrome扩展
- 自动调用OpenClaw Zero Token API获取凭证
- 自动安装Page Agent扩展
- 自动配置LLM API Key（免API）

---

## 三大指令

| 指令 | 用途 |
|------|------|
| /新建应用 | 全新开发 |
| /优化 | 功能优化 |
| /修复 | BUG修复 |
| /检查更新 | 检查技能新版本 |
| /浏览器操作 | 调用浏览器执行自动化任务 |
| /安装扩展 | 自动安装Page Agent扩展并配置LLM |
| /配置AI | 配置免费AI模型（基于OpenClaw Zero Token） |

---

## 免API AI配置 (/配置AI)

### 什么是 OpenClaw Zero Token？
OpenClaw Zero Token 是免 API Token 使用大模型的分支，通过浏览器登录方式**免费**使用各大AI平台。

### 支持的免费AI平台

| 平台 | 模型 | 状态 |
|------|------|------|
| DeepSeek | deepseek-chat, deepseek-reasoner | ✅ 已测试 |
| 千问国际版 | Qwen 3.5 Plus, Qwen 3.5 Turbo | ✅ 已测试 |
| 千问国内版 | Qwen 3.5 Plus, Qwen 3.5 Turbo | ✅ 已测试 |
| Kimi | Moonshot v1 8K/32K/128K | ✅ 已测试 |
| Claude Web | claude-sonnet-4-6, claude-opus-4-6 | ✅ 已测试 |
| 豆包 | doubao-seed-2.0, doubao-pro | ✅ 已测试 |
| ChatGPT Web | GPT-4, GPT-4 Turbo | ✅ 已测试 |
| Gemini Web | Gemini Pro, Gemini Ultra | ✅ 已测试 |
| Grok Web | Grok 1, Grok 2 | ✅ 已测试 |
| 智谱清言 | glm-4-Plus, glm-4-Think | ✅ 已测试 |

### /配置AI 自动流程
1. 检查 OpenClaw Zero Token 是否已配置
2. 自动获取 API 凭证
3. 选择要启用的AI平台
4. 自动配置 LLM 环境变量

### 手动配置流程
1. 在 Chrome 中登录目标AI平台
2. 使用 /安装扩展 自动配置
3. 开始使用免费AI

---

## 浏览器自动化功能

### 使用方式
1. 使用 /安装扩展 自动配置（推荐）
2. 或手动安装 Chrome 扩展：[Page Agent Extension](https://chromewebstore.google.com/detail/page-agent-ext/akldabonmimlicnjlflnapfeklbfemhj)
3. 配置 LLM API（支持 OpenAI 兼容接口）
4. 使用 /浏览器操作 + 自然语言描述任务

### /安装扩展 - 自动配置流程
1. 获取 OpenClaw Zero Token 的 API 凭证
2. 自动安装 Page Agent Chrome 扩展
3. 自动配置 LLM API Key
4. 完成初始化

### 支持的操作
- 打开网页并操作
- 点击按钮、输入文字
- 提取页面内容
- 复制AI回复
- 自动化填表
- 多页面任务

### 环境变量（自动获取）
```
# OpenClaw Zero Token API（免API）
OPENCLAW_API_URL=http://localhost:3002
OPENCLAW_API_KEY=<自动获取>

# LLM配置（免费使用）
LLM_BASE_URL=<自动配置>
LLM_API_KEY=<自动获取>
LLM_MODEL_NAME=qwen3.5-plus
```

---

## OpenClaw Zero Token 集成

### 什么是免API？
传统方式需要购买 API Token，按调用次数计费。Zero Token 方式：
- ✅ **完全免费** - 无需购买 API Token
- ✅ **无使用限制** - 不按次数计费
- ✅ **仅需网页登录** - 不需要绑定信用卡
- ✅ **凭证本地存储** - 更安全

### 技术架构
```
┌─────────────────────────────────────┐
│   miaoda-coop-control 技能          │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  │
│  │ Page Agent │  │ OpenClaw   │  │
│  │ (浏览器控制) │  │ Zero Token │  │
│  └──────┬──────┘  └──────┬──────┘  │
│         │                │          │
│         └────────┬───────┘          │
│                  ▼                  │
│         ┌────────────────┐           │
│         │ 免费 AI 大模型 │           │
│         │ DeepSeek/豆包 │           │
│         │ Kimi/Claude  │           │
│         └────────────────┘           │
└─────────────────────────────────────┘
```

### 使用流程
1. **启动服务** - 运行 OpenClaw Zero Token
2. **登录AI平台** - 在浏览器中登录目标平台
3. **配置AI** - 使用 /配置AI 指令
4. **开始使用** - 浏览器自动化 + 免费AI

---

## 自动更新功能

### 检查更新
- 用户发送：/检查更新
- 自动检测GitHub最新版本
- 对比当前版本
- 显示更新内容

### 更新提醒
```
【技能更新提醒】
当前版本：0.1.0
最新版本：0.2.0
更新内容：xxx
请运行 /更新技能 升级
```

### 更新指令
- /检查更新 - 检查新版本
- /更新技能 - 执行更新

---

## 发布规则

**重要：必须等秒哒开发完成才能发布！**

| 秒哒状态 | 能否发布 |
|----------|----------|
| 阅读中 | ❌ 不能 |
| 开发中 | ❌ 不能 |
| 开发完成 | ✅ 提醒手动发布 |

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| 0.2.0 | 2026-03-18 | 集成OpenClaw Zero Token，支持免API使用AI大模型 |
| 0.1.1 | 2026-03-18 | 集成Page Agent自动安装扩展功能，自动获取OpenClaw API凭证 |
| 1.3.0 | 2026-03-18 | 集成Page Agent浏览器自动化功能 |
| 0.1.0 | 2026-03-16 | 初始版本+自动更新 |

---

## 更新日志

- 2026-03-18: 集成OpenClaw Zero Token，支持免API使用DeepSeek、豆包、Kimi、Claude Web等
- 2026-03-18: 集成Page Agent自动安装扩展功能，自动获取OpenClaw Zero Token API凭证
- 2026-03-18: 集成阿里Page Agent，支持浏览器自动化操作、自然语言控制网页、复制AI回复内容
- 2026-03-16: 初始版本发布
