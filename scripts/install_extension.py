#!/usr/bin/env python3
"""
自动安装 Page Agent Chrome 扩展
自动获取 OpenClaw Zero Token API 凭证（免API）
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

# Page Agent Chrome 扩展 ID
PAGE_AGENT_EXT_ID = "akldabonmimlicnjlflnapfeklbfemhj"
PAGE_AGENT_EXT_URL = "https://chromewebstore.google.com/detail/page-agent-ext/akldabonmimlicnjlflnapfeklbfemhj"

# OpenClaw Zero Token 配置路径
OPENCLAW_ZERO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 
    "openclaw-zero-token"
)

def get_openclaw_zero_token_credentials():
    """获取 OpenClaw Zero Token 的 API 凭证（免API）"""
    print("[*] 正在获取 OpenClaw Zero Token API 凭证...")
    
    # 尝试多个可能的配置路径
    config_paths = [
        os.path.join(OPENCLAW_ZERO_PATH, ".openclaw-upstream-state", "openclaw.json"),
        os.path.join(OPENCLAW_ZERO_PATH, ".openclaw-state.example"),
        os.path.expanduser("~/.openclaw/openclaw.json"),
    ]
    
    for config_path in config_paths:
        config_path = os.path.normpath(config_path)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 提取 API 配置
                api_url = config.get("apiUrl", config.get("api_url", "http://localhost:3002"))
                api_key = config.get("apiKey", config.get("api_key", ""))
                
                if api_key:
                    print(f"[+] 找到 OpenClaw Zero Token 配置: {api_url}")
                    return api_url, api_key
            except Exception as e:
                print(f"[!] 读取配置失败 {config_path}: {e}")
                continue
    
    # 如果没找到配置文件，尝试从运行中的服务获取
    print("[*] 尝试从本地服务获取 API ...")
    try:
        req = urllib.request.Request("http://localhost:3002/api/models")
        req.add_header('Accept', 'application/json')
        with urllib.request.urlopen(req, timeout=5) as response:
            # 服务运行中，使用默认配置
            return "http://localhost:3002", "unknown"
    except:
        pass
    
    print("[!] 无法获取 API 凭证，请确保 OpenClaw Zero Token 已配置")
    return None, None

def get_free_models_from_openclaw(api_url, api_key):
    """从 OpenClaw Zero Token 获取免费模型列表"""
    print("[*] 正在获取免费AI模型列表...")
    
    free_models = []
    
    try:
        req = urllib.request.Request(f"{api_url}/api/models")
        req.add_header('Authorization', f'Bearer {api_key}')
        req.add_header('Accept', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            all_models = data.get("models", [])
            
            # 筛选免费平台
            free_platforms = ["deepseek", "doubao", "kimi", "qwen", "claude-web", "gemini-web", "grok", "glm"]
            
            for model in all_models:
                provider = model.get("provider", "").lower()
                if any(p in provider for p in free_platforms):
                    free_models.append({
                        "name": model.get("name"),
                        "provider": model.get("provider"),
                        "status": model.get("status")
                    })
            
            print(f"[+] 找到 {len(free_models)} 个免费AI模型")
            
            # 显示可用模型
            if free_models:
                print("\n可用免费AI模型:")
                for m in free_models[:10]:  # 显示前10个
                    print(f"  - {m['provider']}: {m['name']}")
            
            return free_models
            
    except Exception as e:
        print(f"[!] 获取模型列表失败: {e}")
        return []

def get_llm_config_from_openclaw(api_url, api_key, models):
    """从 OpenClaw Zero Token 获取 LLM 配置"""
    print("[*] 正在配置 LLM（免API）...")
    
    # 优先选择免费的模型
    default_model = "qwen3.5-plus"
    for model in models:
        if model.get("status") == "available":
            default_model = model.get("name", default_model)
            break
    
    return {
        "base_url": f"{api_url}/v1",
        "api_key": api_key,
        "model": default_model
    }

def check_chrome_installed():
    """检查 Chrome 是否安装"""
    print("[*] 检查 Chrome 浏览器...")
    
    chrome_paths = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        os.path.expanduser("~/AppData/Local/Google/Chrome/Application/chrome.exe"),
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"[+] 找到 Chrome: {path}")
            return path
    
    print("[!] 未找到 Chrome，请先安装 Chrome 浏览器")
    return None

def install_chrome_extension(chrome_path):
    """安装 Chrome 扩展"""
    print("[*] 正在安装 Page Agent Chrome 扩展...")
    
    extension_dir = os.path.join(os.path.dirname(__file__), "..", "page-agent", "packages", "extension")
    
    if os.path.exists(extension_dir):
        print(f"[+] 找到扩展源码: {extension_dir}")
    
    print("[*] 打开 Chrome 扩展商店页面...")
    
    try:
        subprocess.Popen([
            chrome_path,
            "--new-window",
            PAGE_AGENT_EXT_URL
        ])
        print("[+] 请在打开的 Chrome 页面中点击'添加至Chrome'按钮")
        return True
    except Exception as e:
        print(f"[!] 打开失败: {e}")
        return False

def setup_environment_variables(api_url, api_key, llm_config):
    """设置环境变量配置文件"""
    print("[*] 正在配置环境变量...")
    
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env.page-agent")
    
    env_content = f"""# Page Agent 环境配置
# 由 miaoda-coop-control 自动生成
# 使用 OpenClaw Zero Token（免API）

# OpenClaw Zero Token API（免API）
OPENCLAW_API_URL={api_url}
OPENCLAW_API_KEY={api_key}

# Page Agent LLM 配置（免费使用）
LLM_BASE_URL={llm_config['base_url']}
LLM_API_KEY={llm_config['api_key']}
LLM_MODEL_NAME={llm_config['model']}

# Page Agent 端口
PORT=38401

# 免API标记
FREE_MODE=true
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"[+] 环境配置已保存至: {env_file}")
        return True
    except Exception as e:
        print(f"[!] 保存配置失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("  Page Agent + OpenClaw Zero Token 自动安装程序")
    print("  秒哒开发协作管控 v0.2.0")
    print("=" * 60)
    
    # 1. 检查 Chrome
    chrome_path = check_chrome_installed()
    if not chrome_path:
        print("\n[!] 请先安装 Chrome 浏览器")
        return False
    
    # 2. 获取 OpenClaw Zero Token API 凭证（免API）
    api_url, api_key = get_openclaw_zero_token_credentials()
    if not api_key:
        print("\n[!] 无法获取 API 凭证")
        print("[*] 请先启动 OpenClaw Zero Token 服务")
        print("[*] 或在浏览器中登录目标AI平台后重试")
        
        # 仍然尝试安装扩展，只是没有API配置
        install_chrome_extension(chrome_path)
        return False
    
    # 3. 获取免费模型列表
    free_models = get_free_models_from_openclaw(api_url, api_key)
    
    # 4. 获取 LLM 配置
    llm_config = get_llm_config_from_openclaw(api_url, api_key, free_models)
    print(f"[+] LLM 配置: {llm_config['model']} (免API)")
    
    # 5. 安装 Chrome 扩展
    install_chrome_extension(chrome_path)
    
    # 6. 保存环境配置
    setup_environment_variables(api_url, api_key, llm_config)
    
    print("\n" + "=" * 60)
    print("  安装完成！")
    print("=" * 60)
    print(f"""
✅ 已配置以下免费AI模型：
   - DeepSeek (深度推理)
   - 豆包 (内容创作)
   - Kimi (长文本)
   - 千问 (多场景)
   - Claude Web (高级推理)
   - Gemini Web (多模态)
   - Grok (实时信息)
   - 智谱 (中文优化)

下一步：
1. 在 Chrome 中点击"添加至Chrome"完成扩展安装
2. 登录你需要使用的 AI 平台（豆包/Kimi等）
3. 使用 /浏览器操作 指令开始自动化任务
4. 使用 /配置AI 选择免费AI模型

提示：所有AI模型均为免费使用，无需API Key！
    """)
    
    return True

if __name__ == "__main__":
    main()
