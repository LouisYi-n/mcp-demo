"""
Ollama API Service - Ollama API服务
负责与本地Ollama服务通信
"""

import requests
import logging

def ask_ollama(prompt: str) -> str:
    """直接调用 Ollama API 使用 deepseek-r1-7b 模型"""
    try:
        data = {
            "model": "deepseek-r1:7b",
            "prompt": prompt,
            "stream": False
        }
        
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if resp.status_code == 200:
            result = resp.json()
            return result.get("response", "未获取到模型回复")
        else:
            return f"Ollama 服务错误: {resp.status_code}"
    except Exception as e:
        logging.error(f"Ollama 服务异常: {e}")
        return f"Ollama 服务异常: {e}" 