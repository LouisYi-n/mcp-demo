"""
Configuration - 配置文件
包含应用程序的各种配置选项
"""

import logging

# 服务配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
FLASK_DEBUG = True

# Ollama 配置
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "deepseek-r1:7b"

# 天气API配置
WEATHER_API_BASE_URL = "http://localhost:8081"
WEATHER_API_TIMEOUT = 10

# 日志配置
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

# 应用信息
APP_NAME = "zdlang-agent"
APP_DESCRIPTION = "智能代理：使用AI路由自动识别意图并调用相应工具"
APP_VERSION = "1.0.0"

# 依赖服务
DEPENDENCIES = {
    "ollama": OLLAMA_BASE_URL,
    "mcp-server": WEATHER_API_BASE_URL
} 