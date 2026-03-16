---
name: miaoda-coop-control
version: 1.3.0
description: |
  秒哒开发协作管控 - 自动化执行版。包含完整Python脚本实现真正的自动化。
  版权: 米乐 | 版本: 1.3.0
  触发条件：(1) /新建应用 (2) /优化 (3) /修复
---

# 秒哒开发协作管控 v1.3.0 自动化执行版

## 技能状态

**文档版本：** v1.2.0
**代码版本：** v1.3.0 (新增完整Python脚本)

## 文件结构

```
miaoda-coop-control/
├── SKILL.md              # 技能说明文档
├── README.md            # GitHub介绍
├── scripts/
│   ├── main.py          # 主程序入口
│   ├── browser_ops.py   # 浏览器自动化操作
│   ├── task_queue.py   # 需求队列模块
│   └── app_manager.py  # 应用管理模块
└── data/                # 数据存储目录
    ├── apps.json        # 应用信息
    ├── task_queue.json  # 任务队列
    └── task_status.json # 任务状态
```

## 核心功能

### 1. 主程序 main.py
- 解析用户指令 (/新建应用、/优化、/修复)
- 调度各模块执行
- 管理任务流程

### 2. 浏览器自动化 browser_ops.py
- 打开AI官网（豆包/Kimi等）
- 切换思考模式
- 输入需求
- 等待生成
- 转为文档
- 下载文档

### 3. 需求队列 task_queue.py
- 任务状态管理（空闲/繁忙）
- 需求缓存与合并
- 自动去重

### 4. 应用管理 app_manager.py
- 应用ID生成
- 状态跟踪
- URL管理

## 使用方式

```bash
# 运行主程序
python scripts/main.py

# 或导入使用
from scripts.main import MiaodaController

controller = MariaController()
result = controller.run("/新建应用 开发一个企业官网")
```

## 配置

在 main.py 中配置：
- API_KEY: 秒哒API密钥
- DOCS_DIR: 文档保存目录

## 版本历史

- v1.3.0 (2026-03-16): 自动化执行版
- v1.2.0 (2026-03-16): 需求队列缓存合并
- v1.1.0 (2026-03-16): 多AI模型支持
- v1.0.0: 初始版本
