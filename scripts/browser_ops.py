# 浏览器操作模块
"""
浏览器自动化操作 - 调用豆包/Kimi等AI生成需求 + Page Agent 自动化 + OpenClaw Zero Token 免API
需要配合 Playwright 或 Page Agent 扩展使用
支持免API使用AI大模型（DeepSeek、豆包、Kimi、Claude Web等）
"""

import time
import subprocess
import os
import json
import urllib.request
import urllib.error

# OpenClaw Zero Token 配置路径
OPENCLAW_ZERO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 
    "openclaw-zero-token"
)

class OpenClawZeroToken:
    """OpenClaw Zero Token 免API调用类"""
    
    def __init__(self):
        self.api_url = "http://localhost:3002"
        self.api_key = ""
        self.available_models = []
        self._load_config()
    
    def _load_config(self):
        """加载OpenClaw Zero Token配置"""
        config_paths = [
            os.path.join(OPENCLAW_ZERO_PATH, ".openclaw-upstream-state", "openclaw.json"),
            os.path.join(OPENCLAW_ZERO_PATH, ".openclaw-state.example"),
            os.path.expanduser("~/.openclaw/openclaw.json"),
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    self.api_url = config.get("apiUrl", self.api_url)
                    self.api_key = config.get("apiKey", "")
                    print(f"[OpenClaw Zero Token] 加载配置: {self.api_url}")
                    return
                except Exception as e:
                    print(f"[!] 读取配置失败: {e}")
        
        print("[!] 未找到OpenClaw Zero Token配置")
    
    def check_service(self):
        """检查服务是否运行"""
        try:
            req = urllib.request.Request(f"{self.api_url}/api/models")
            req.add_header('Accept', 'application/json')
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                self.available_models = data.get("models", [])
                print(f"[✓] OpenClaw Zero Token 服务运行中")
                print(f"[✓] 可用模型: {len(self.available_models)} 个")
                return True
        except Exception as e:
            print(f"[!] OpenClaw Zero Token 服务未运行: {e}")
            return False
    
    def get_free_models(self):
        """获取可用的免费模型列表"""
        free_providers = ["deepseek", "doubao", "kimi", "qwen", "claude-web", "gemini-web", "grok", "glm"]
        free_models = []
        
        for model in self.available_models:
            provider = model.get("provider", "").lower()
            if any(p in provider for p in free_providers):
                free_models.append({
                    "name": model.get("name"),
                    "provider": model.get("provider"),
                    "status": model.get("status")
                })
        
        return free_models
    
    def get_api_config(self):
        """获取API配置供Page Agent使用"""
        return {
            "base_url": f"{self.api_url}/v1",
            "api_key": self.api_key,
            "models": self.get_free_models()
        }


class BrowserAutomation:
    """浏览器自动化操作类"""
    
    def __init__(self):
        self.browser = None
        self.page = None
        self.page_agent_available = False
        self.openclaw_zero = OpenClawZeroToken()
        self._check_page_agent()
        
    def _check_page_agent(self):
        """检查Page Agent是否可用"""
        page_agent_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "page-agent"
        )
        if os.path.exists(page_agent_path):
            self.page_agent_available = True
            print("[浏览器] Page Agent 已集成 ✓")
        else:
            print("[浏览器] Page Agent 未安装，将使用基础浏览器操作")
    
    def check_openclaw_zero_token(self):
        """检查OpenClaw Zero Token是否可用"""
        return self.openclaw_zero.check_service()
    
    def get_free_ai_models(self):
        """获取可用的免费AI模型"""
        return self.openclaw_zero.get_free_models()
    
    def get_page_agent_config(self):
        """获取Page Agent配置（使用OpenClaw Zero Token）"""
        oc_config = self.openclaw_zero.get_api_config()
        
        # 优先选择免费的模型
        models = oc_config.get("models", [])
        default_model = "qwen3.5-plus"
        
        if models:
            default_model = models[0].get("name", default_model)
        
        return {
            "llm_base_url": oc_config["base_url"],
            "llm_api_key": oc_config["api_key"],
            "llm_model": default_model,
            "port": 38401,
            "free": True  # 标记为免费使用
        }
    
    async def execute_with_page_agent(self, task: str) -> str:
        """
        使用Page Agent执行浏览器任务
        需要先安装Chrome扩展并配置LLM
        """
        if not self.page_agent_available:
            return "[错误] Page Agent未安装，请先安装page-agent技能"
        
        config = self.get_page_agent_config()
        if not config["llm_api_key"]:
            return "[错误] 请配置LLM_API_KEY环境变量"
        
        # 使用MCP协议调用Page Agent
        # 这里需要启动@page-agent/mcp服务
        try:
            result = await self._call_mcp_server(task, config)
            return result
        except Exception as e:
            return f"[错误] Page Agent执行失败: {str(e)}"
    
    async def _call_mcp_server(self, task: str, config: dict) -> str:
        """调用MCP服务器的execute_task工具"""
        # MCP工具调用实现
        # 这里是一个示例，实际需要通过stdio启动MCP服务器
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "execute_task",
                "arguments": {"task": task}
            }
        }
        
        # 启动MCP服务器作为子进程
        env = {
            **os.environ,
            "LLM_BASE_URL": config["llm_base_url"],
            "LLM_API_KEY": config["llm_api_key"],
            "LLM_MODEL_NAME": config["llm_model"],
            "PORT": str(config["port"])
        }
        
        # 启动page-agent mcp服务
        proc = await subprocess.create_subprocess_exec(
            "npx", "-y", "@page-agent/mcp",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        
        # 发送请求
        proc.stdin.write(json.dumps(mcp_request).encode())
        await proc.stdin.drain()
        
        # 读取响应
        response = await proc.stdout.readline()
        await proc.wait()
        
        if response:
            result = json.loads(response)
            if "result" in result:
                return result["result"]["content"][0]["text"]
        
        return "[错误] 未获得有效响应"
    
    def open_doubao(self):
        """打开豆包网页版"""
        print("[浏览器] 打开豆包网页版...")
        # 实际实现需要启动浏览器
        # subprocess.run(["start", "chrome", "https://www.doubao.com"], shell=True)
        pass
    
    def switch_to_think_mode(self):
        """切换到思考模式"""
        print("[浏览器] 切换到思考模式...")
        # 需要定位并点击思考模式按钮
        pass
    
    def input_requirement(self, text):
        """输入需求内容"""
        print(f"[浏览器] 输入需求: {text[:50]}...")
        # 需要定位输入框并输入文字
        pass
    
    def wait_for_response(self, timeout=120):
        """等待AI生成完成"""
        print(f"[浏览器] 等待AI响应 (超时{timeout}秒)...")
        # 需要轮询检查AI是否生成完成
        time.sleep(5)  # 简化
        return True
    
    def click_three_dots(self):
        """点击三个点按钮"""
        print("[浏览器] 点击三个点按钮...")
        # 需要定位并点击底部三点按钮
        pass
    
    def click_convert_to_doc(self):
        """点击转为文档"""
        print("[浏览器] 选择'转为文档编辑'...")
        # 需要在菜单中选择
        pass
    
    def click_download(self):
        """点击下载按钮"""
        print("[浏览器] 点击下载按钮...")
        # 需要定位并点击下载
        pass
    
    def get_generated_content(self):
        """获取生成的内容"""
        print("[浏览器] 获取生成的内容...")
        # 需要获取页面文本内容
        return ""
    
    def close(self):
        """关闭浏览器"""
        print("[浏览器] 关闭浏览器...")
        if self.browser:
            self.browser.close()
    
    def run_full_flow(self, requirement):
        """
        完整执行流程
        1. 打开AI网页
        2. 输入需求
        3. 等待生成
        4. 获取内容
        5. 转为文档
        6. 下载文档
        """
        try:
            # 1. 打开
            self.open_doubao()
            time.sleep(3)
            
            # 2. 切换思考模式
            self.switch_to_think_mode()
            time.sleep(1)
            
            # 3. 输入需求
            self.input_requirement(requirement)
            time.sleep(1)
            
            # 4. 提交并等待
            print("[浏览器] 提交需求，等待生成...")
            self.wait_for_response()
            
            # 5. 获取内容
            content = self.get_generated_content()
            
            # 6. 转为文档
            self.click_three_dots()
            time.sleep(1)
            self.click_convert_to_doc()
            time.sleep(2)
            self.click_download()
            
            return content
            
        except Exception as e:
            print(f"[浏览器] 执行出错: {e}")
            return None
        finally:
            self.close()
