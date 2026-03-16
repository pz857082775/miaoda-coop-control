# 任务状态管理脚本

import json
import os
from datetime import datetime
from pathlib import Path

# 配置路径
TASK_DIR = Path("memory/miaoda-tasks")
TASK_DIR.mkdir(parents=True, exist_ok=True)

# 任务状态
TASK_STATES = {
    "pending": "待开发",
    "developing": "开发中", 
    "testing": "测试中",
    "need_fix": "需修复",
    "completed": "已完成"
}

class TaskManager:
    """秒哒开发任务管理器"""
    
    def __init__(self):
        self.current_task = None
        self.task_queue = []
    
    def add_task(self, app_name: str, requirement: str) -> str:
        """添加新任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        task = {
            "id": task_id,
            "app_name": app_name,
            "requirement": requirement,
            "state": "pending",
            "created_at": datetime.now().isoformat(),
            "state_history": [{
                "from": "none",
                "to": "pending",
                "timestamp": datetime.now().isoformat(),
                "trigger": "需求提交"
            }]
        }
        
        # 保存任务
        with open(TASK_DIR / f"{task_id}.json", "w", encoding="utf-8") as f:
            json.dump(task, f, ensure_ascii=False, indent=2)
        
        return task_id
    
    def get_task_state(self, task_id: str) -> str:
        """获取任务当前状态"""
        try:
            with open(TASK_DIR / f"{task_id}.json", "r", encoding="utf-8") as f:
                task = json.load(f)
            return task.get("state", "unknown")
        except:
            return "not_found"
    
    def change_state(self, task_id: str, new_state: str, trigger: str, note: str = "") -> bool:
        """变更任务状态"""
        current_state = self.get_task_state(task_id)
        
        # 检查是否可转换
        if not self.can_transition(current_state, new_state):
            return False
        
        # 读取并更新任务
        try:
            with open(TASK_DIR / f"{task_id}.json", "r", encoding="utf-8") as f:
                task = json.load(f)
            
            task["state"] = new_state
            task["state_history"].append({
                "from": current_state,
                "to": new_state,
                "timestamp": datetime.now().isoformat(),
                "trigger": trigger,
                "note": note
            })
            
            with open(TASK_DIR / f"{task_id}.json", "w", encoding="utf-8") as f:
                json.dump(task, f, ensure_ascii=False, indent=2)
            
            return True
        except:
            return False
    
    def can_transition(self, from_state: str, to_state: str) -> bool:
        """检查状态转换是否合法"""
        # 定义合法的状态转换
        valid_transitions = {
            "pending": ["developing"],
            "developing": ["testing"],
            "testing": ["need_fix", "completed"],
            "need_fix": ["testing"],
            "completed": []
        }
        return to_state in valid_transitions.get(from_state, [])
    
    def get_current_task(self) -> dict:
        """获取当前进行中的任务"""
        for task_file in TASK_DIR.glob("*.json"):
            with open(task_file, "r", encoding="utf-8") as f:
                task = json.load(f)
            if task["state"] in ["developing", "testing", "need_fix"]:
                return task
        return None
    
    def is_busy(self) -> bool:
        """检查是否有任务正在进行"""
        current = self.get_current_task()
        return current is not None
    
    def add_bug(self, task_id: str, bug_info: dict) -> bool:
        """记录BUG"""
        try:
            with open(TASK_DIR / f"{task_id}.json", "r", encoding="utf-8") as f:
                task = json.load(f)
            
            if "bugs" not in task:
                task["bugs"] = []
            
            bug_info["id"] = len(task["bugs"]) + 1
            bug_info["created_at"] = datetime.now().isoformat()
            task["bugs"].append(bug_info)
            
            with open(TASK_DIR / f"{task_id}.json", "w", encoding="utf-8") as f:
                json.dump(task, f, ensure_ascii=False, indent=2)
            
            return True
        except:
            return False

# 全局实例
task_manager = TaskManager()
