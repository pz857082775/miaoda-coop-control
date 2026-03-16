# 应用管理模块
"""
应用全生命周期管理
存储应用ID、名称、状态、链接等信息
"""

import json
import os
from datetime import datetime
from pathlib import Path

class AppManager:
    """应用管理类"""
    
    def __init__(self, apps_file="apps.json"):
        self.apps_file = apps_file
        self.apps = self.load_apps()
        
    def load_apps(self):
        """加载应用列表"""
        if os.path.exists(self.apps_file):
            with open(self.apps_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def save_apps(self):
        """保存应用列表"""
        with open(self.apps_file, "w", encoding="utf-8") as f:
            json.dump(self.apps, f, ensure_ascii=False, indent=2)
    
    def create_app(self, app_id, app_name, app_type="WEB"):
        """创建新应用"""
        self.apps[app_id] = {
            "id": app_id,
            "name": app_name,
            "type": app_type,
            "status": "待开发",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "dev_url": None,
            "release_url": None,
            "requirements": [],
            "bugs": []
        }
        self.save_apps()
        print(f"[应用] 创建应用: {app_id} - {app_name}")
        return self.apps[app_id]
    
    def get_app(self, app_id):
        """获取应用信息"""
        return self.apps.get(app_id)
    
    def update_status(self, app_id, status):
        """更新应用状态"""
        if app_id in self.apps:
            self.apps[app_id]["status"] = status
            self.apps[app_id]["updated_at"] = datetime.now().isoformat()
            self.save_apps()
            print(f"[应用] 更新状态: {app_id} -> {status}")
    
    def add_requirement(self, app_id, requirement):
        """添加需求"""
        if app_id in self.apps:
            self.apps[app_id]["requirements"].append({
                "content": requirement,
                "added_at": datetime.now().isoformat()
            })
            self.apps[app_id]["updated_at"] = datetime.now().isoformat()
            self.save_apps()
    
    def add_bug(self, app_id, bug):
        """添加BUG记录"""
        if app_id in self.apps:
            self.apps[app_id]["bugs"].append({
                "description": bug,
                "added_at": datetime.now().isoformat()
            })
            self.apps[app_id]["updated_at"] = datetime.now().isoformat()
            self.save_apps()
    
    def update_urls(self, app_id, dev_url=None, release_url=None):
        """更新URL"""
        if app_id in self.apps:
            if dev_url:
                self.apps[app_id]["dev_url"] = dev_url
            if release_url:
                self.apps[app_id]["release_url"] = release_url
            self.apps[app_id]["updated_at"] = datetime.now().isoformat()
            self.save_apps()
    
    def list_apps(self, status=None):
        """列出应用"""
        if status:
            return [app for app in self.apps.values() if app["status"] == status]
        return list(self.apps.values())
    
    def delete_app(self, app_id):
        """删除应用"""
        if app_id in self.apps:
            del self.apps[app_id]
            self.save_apps()
            print(f"[应用] 删除应用: {app_id}")
    
    def search_by_name(self, keyword):
        """按名称搜索"""
        results = []
        for app in self.apps.values():
            if keyword.lower() in app.get("name", "").lower():
                results.append(app)
        return results


# 测试
if __name__ == "__main__":
    manager = AppManager()
    
    # 创建测试应用
    app = manager.create_app("APP-001", "测试企业官网", "WEB")
    print(app)
    
    # 更新状态
    manager.update_status("APP-001", "开发中")
    
    # 添加需求
    manager.add_requirement("APP-001", "需要首页轮播图")
    
    # 列出所有
    print(manager.list_apps())
