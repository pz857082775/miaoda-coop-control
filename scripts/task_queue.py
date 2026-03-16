# 需求队列模块
"""
需求队列缓存与合并模块
秒哒繁忙时自动收集需求，合并后执行
"""

import json
import os
from datetime import datetime
from pathlib import Path

class TaskQueue:
    """需求队列管理"""
    
    def __init__(self, queue_file="task_queue.json"):
        self.queue_file = queue_file
        self.queue = self.load_queue()
        
    def load_queue(self):
        """加载队列"""
        if os.path.exists(self.queue_file):
            with open(self.queue_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    
    def save_queue(self):
        """保存队列"""
        with open(self.queue_file, "w", encoding="utf-8") as f:
            json.dump(self.queue, f, ensure_ascii=False, indent=2)
    
    def add_task(self, task):
        """添加任务到队列"""
        task["timestamp"] = datetime.now().isoformat()
        task["id"] = len(self.queue) + 1
        self.queue.append(task)
        self.save_queue()
        print(f"[队列] 添加任务: {task.get('type')} - {task.get('requirement', task.get('app_id', ''))[:30]}")
        
    def get_tasks_by_app(self, app_id):
        """获取同一应用的所有任务"""
        return [t for t in self.queue if t.get("app_id") == app_id]
    
    def merge_tasks(self, app_id):
        """合并同一应用的任务"""
        tasks = self.get_tasks_by_app(app_id)
        if not tasks:
            return None
        
        # 合并需求内容
        merged_content = []
        for task in tasks:
            if task.get("type") == "new":
                merged_content.append(f"新建: {task.get('requirement', '')}")
            elif task.get("type") == "optimize":
                merged_content.append(f"优化: {task.get('requirement', '')}")
            elif task.get("type") == "fix":
                merged_content.append(f"修复: {task.get('bug', '')}")
        
        return "\n".join(merged_content)
    
    def remove_tasks_by_app(self, app_id):
        """清除某应用的所有任务"""
        self.queue = [t for t in self.queue if t.get("app_id") != app_id]
        self.save_queue()
        print(f"[队列] 清除应用 {app_id} 的任务")
    
    def get_all_tasks(self):
        """获取所有任务"""
        return self.queue
    
    def is_empty(self):
        """队列是否为空"""
        return len(self.queue) == 0
    
    def get_next_task(self):
        """获取下一个任务"""
        if self.queue:
            return self.queue[0]
        return None
    
    def clear(self):
        """清空队列"""
        self.queue = []
        self.save_queue()
        print("[队列] 队列已清空")


class TaskStatus:
    """任务状态管理"""
    
    def __init__(self, status_file="task_status.json"):
        self.status_file = status_file
        self.status = self.load_status()
        
    def load_status(self):
        """加载状态"""
        if os.path.exists(self.status_file):
            with open(self.status_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"state": "idle", "current_app": None, "start_time": None}
    
    def save_status(self):
        """保存状态"""
        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(self.status, f, ensure_ascii=False, indent=2)
    
    def is_idle(self):
        """是否空闲"""
        return self.status.get("state") == "idle"
    
    def set_busy(self, app_id):
        """设置为繁忙"""
        self.status["state"] = "busy"
        self.status["current_app"] = app_id
        self.status["start_time"] = datetime.now().isoformat()
        self.save_status()
        print(f"[状态] 秒哒开始处理: {app_id}")
    
    def set_idle(self):
        """设置为空闲"""
        self.status["state"] = "idle"
        self.status["current_app"] = None
        self.status["end_time"] = datetime.now().isoformat()
        self.save_status()
        print("[状态] 秒哒空闲")
    
    def get_current_app(self):
        """获取当前处理的应用"""
        return self.status.get("current_app")
