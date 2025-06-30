"""
Configuration - Configuration File
Contains various configuration options for the application
"""

import logging

# Service Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
FLASK_DEBUG = True

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "deepseek-r1:7b"

# Weather API Configuration
WEATHER_API_BASE_URL = "http://localhost:8081"
WEATHER_API_TIMEOUT = 10

# Logging Configuration
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

# Application Information
APP_NAME = "zdlang-agent"
APP_DESCRIPTION = "Intelligent Agent: Automatically identifies user intent and calls appropriate tools using AI routing"
APP_VERSION = "1.0.0"

# Dependent Services
DEPENDENCIES = {
    "ollama": OLLAMA_BASE_URL,
    "mcp-server": WEATHER_API_BASE_URL
} 