# 秒哒开发协作管控

[![版本](https://img.shields.io/badge/版本-1.3.0-blue)](https://github.com/mile-ai/miaoda-coop-control)
[![版权](https://img.shields.io/badge/版权-米乐-green)](https://github.com/mile-ai)

作为 OpenClaw 的秒哒开发协作管控技能，自动化执行版。

## 核心特性

| 特性 | 说明 |
|------|------|
| **自动化执行** | 完整Python脚本，真正实现自动化 |
| **多AI模型** | 支持豆包、Kimi等 |
| **需求队列** | 繁忙时自动缓存合并 |
| **应用管理** | 全生命周期管理 |

## 文件结构

```
miaoda-coop-control/
├── SKILL.md
├── README.md
└── scripts/
    ├── main.py           # 主程序入口
    ├── browser_ops.py    # 浏览器自动化
    ├── task_queue.py    # 需求队列
    └── app_manager.py   # 应用管理
```

## 功能模块

1. **main.py** - 解析指令、调度任务
2. **browser_ops.py** - 浏览器操作AI生成需求
3. **task_queue.py** - 需求队列与状态管理
4. **app_manager.py** - 应用信息管理

## 使用

```bash
python scripts/main.py
```

## 版本

- v1.3.0 - 自动化执行版
- v1.2.0 - 需求队列
- v1.1.0 - 多AI模型

## 版权

版权所有 © 2026 米乐
