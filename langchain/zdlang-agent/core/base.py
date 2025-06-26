"""
Base classes and interfaces - 基础类和接口定义
"""

from abc import ABC, abstractmethod
from typing import Dict

class ToolHandler(ABC):
    """工具处理器基类"""
    
    @abstractmethod
    def get_tool_name(self) -> str:
        """返回工具名称"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """返回工具描述，用于智能路由"""
        pass
    
    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """简单规则判断是否能处理该查询"""
        pass
    
    @abstractmethod
    def handle(self, query: str) -> Dict[str, str]:
        """处理查询并返回结果"""
        pass 