"""
Services package - 外部服务包
包含与外部API和服务的接口
"""

from .ollama import ask_ollama
from .weather_api import get_weather

__all__ = ['ask_ollama', 'get_weather'] 