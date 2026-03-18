# 秒哒开发协作管控 (miaoda-coop-control)

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/platform-OpenClaw-green" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-orange" alt="License">
  <img src="https://img.shields.io/badge/AI-Free-red" alt="Free AI">
</p>

## 📋 项目简介

秒哒开发协作管控是 OpenClaw 的智能技能，专门用于软件开发任务的自动化管理。通过自然语言指令即可完成应用开发、功能优化、Bug修复等任务，同时支持**免API使用AI大模型**进行浏览器自动化操作。

**版权：** 米乐  
**版本：** 0.2.0  
**发布日期：** 2026-03-18  
**GitHub：** [pz857082775/miaoda-coop-control](https://github.com/pz857082775/miaoda-coop-control)

---

## ✨ 核心特性

### 🎯 三大核心指令

| 指令 | 功能 |
|------|------|
| `/新建应用` | 全新开发应用 |
| `/优化` | 优化现有功能 |
| `/修复` | 修复Bug |

### 🤖 免API AI大模型支持

本技能集成了 **OpenClaw Zero Token**，可以**免费**使用以下AI平台，无需API Key：

| AI模型 | 支持状态 | 模型名称 |
|--------|----------|----------|
| DeepSeek | ✅ 免费 | deepseek-chat, deepseek-reasoner |
| 豆包 | ✅ 免费 | doubao-seed-2.0, doubao-pro |
| Kimi | ✅ 免费 | Moonshot v1 8K/32K/128K |
| 千问 | ✅ 免费 | Qwen 3.5 Plus/Turbo |
| Claude Web | ✅ 免费 | claude-sonnet/opus |
| ChatGPT Web | ✅ 免费 | GPT-4, GPT-4 Turbo |
| Gemini Web | ✅ 免费 | Gemini Pro/Ultra |
| Grok | ✅ 免费 | Grok 1/2 |
| 智谱清言 | ✅ 免费 | glm-4-Plus/Think |

### 🌐 浏览器自动化

基于阿里 **Page Agent** 实现强大的浏览器自动化功能：

- 🔍 智能搜索 - 自动打开网页并搜索内容
- 📝 表单填写 - 自动填写各种网页表单
- 🖱️ 元素操作 - 自动点击按钮、链接
- 📄 内容提取 - 自动提取页面内容
- 📋 复制粘贴 - 自动复制AI回复内容
- 🌐 多页面任务 - 支持复杂的多步骤任务

### ⚡ 自动配置

- `/安装扩展` - 自动安装Page Agent Chrome扩展
- `/配置AI` - 自动配置免费AI模型
- `/检查更新` - 自动检查技能更新

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 确保已安装 OpenClaw
npm install -g openclaw
```

### 2. 安装技能

```bash
# 克隆项目
git clone https://github.com/pz857082775/miaoda-coop-control.git
cd miaoda-coop-control
```

### 3. 配置免API AI（可选）

```bash
# 启动 OpenClaw Zero Token 服务
cd openclaw-zero-token
./server.sh start

# 在浏览器中登录目标AI平台
# 然后使用指令配置
```

### 4. 使用指令

```
# 开发新应用
/新建应用 帮我开发一个TodoList应用

# 优化功能
/优化 优化搜索性能

# 修复Bug
/修复 登录页面闪退

# 配置免费AI
/配置AI

# 安装浏览器扩展
/安装扩展

# 浏览器自动化
/浏览器操作 打开百度搜索OpenClaw
```

---

## 📁 项目结构

```
miaoda-coop-control/
├── SKILL.md                      # 技能定义文件
├── README.md                     # 说明文档
├── data/                         # 数据目录
│   └── apps.json                # 应用数据存储
├── scripts/                      # 脚本目录
│   ├── main.py                  # 主程序入口
│   ├── app_manager.py           # 应用管理模块
│   ├── browser_ops.py           # 浏览器操作（含OpenClaw集成）
│   ├── task_queue.py            # 任务队列
│   └── install_extension.py    # 扩展安装脚本
├── references/                   # 参考文档
│   ├── page-agent.md           # Page Agent集成参考
│   └── openclaw-zero-token.md  # OpenClaw集成参考
└── openclaw-zero-token/         # OpenClaw Zero Token（已集成）
```

---

## 🔧 技术架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│              miaoda-coop-control 技能                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ 任务调度器  │  │  应用管理器  │  │  任务队列   │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │            │
│         └────────────────┼────────────────┘            │
│                          ▼                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │            核心引擎                             │   │
│  └──────────────────┬──────────────────────────────┘   │
│                     │                                    │
│         ┌───────────┴───────────┐                      │
│         ▼                       ▼                      │
│  ┌──────────────┐    ┌────────────────────┐          │
│  │ Page Agent   │    │ OpenClaw Zero      │          │
│  │ (浏览器控制)  │    │     Token          │          │
│  └──────┬───────┘    └─────────┬──────────┘          │
│         │                       │                      │
│         └───────────┬───────────┘                      │
│                     ▼                                    │
│         ┌─────────────────────┐                         │
│         │   免费 AI 大模型     │                         │
│         │ DeepSeek/豆包/Kimi  │                         │
│         │ Claude/Gemini/Grok │                         │
│         └─────────────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

### 核心技术栈

- **Python** - 主要编程语言
- **OpenClaw** - AI Agent 框架
- **Page Agent** - 阿里开源浏览器自动化
- **OpenClaw Zero Token** - 免API调用大模型

---

## 📖 详细功能说明

### 1. 应用管理

- 自动生成唯一应用ID
- 状态跟踪（开发中/已完成）
- 版本记录

### 2. 任务队列

- 需求自动收集
- 智能合并重复请求
- 优先级调度

### 3. 免API调用

**传统方式 vs Zero Token 方式：**

| 对比项 | 传统API | Zero Token |
|--------|---------|------------|
| 费用 | 按调用付费 | 完全免费 |
| 限制 | 有次数限制 | 无限制 |
| 信用卡 | 需要绑定 | 仅需登录网页 |
| 安全性 | API可能泄露 | 凭证本地存储 |

### 4. 浏览器自动化示例

```python
# 浏览器操作示例
from scripts.browser_ops import BrowserAutomation

browser = BrowserAutomation()

# 检查OpenClaw Zero Token服务
browser.check_openclaw_zero_token()

# 获取免费AI模型
models = browser.get_free_ai_models()
print(models)

# 获取Page Agent配置
config = browser.get_page_agent_config()
print(config)
```

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 0.2.0 | 2026-03-18 | 集成OpenClaw Zero Token，支持免API使用AI大模型 |
| 0.1.1 | 2026-03-18 | 集成Page Agent自动安装扩展功能 |
| 0.1.0 | 2026-03-16 | 初始版本发布 |

---

## ⚠️ 注意事项

1. **浏览器要求** - 需要安装 Chrome 浏览器
2. **扩展权限** - Page Agent 需要访问页面内容的权限
3. **首次使用** - 需要在浏览器中登录目标AI平台一次
4. **服务运行** - 浏览器自动化需要 OpenClaw Zero Token 服务运行

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

MIT License - 免费开源，欢迎使用

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
- [Page Agent](https://github.com/alibaba/page-agent) - 阿里开源浏览器自动化
- [OpenClaw Zero Token](https://github.com/linuxhsj/openclaw-zero-token) - 免API解决方案

---

<p align="center">Made with ❤️ by 米乐</p>
<p align="center">免API AI 驱动 | 浏览器自动化新时代</p>
