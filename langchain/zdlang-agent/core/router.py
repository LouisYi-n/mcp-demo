"""
Smart Router - 智能路由器
负责将用户查询路由到合适的工具处理器
"""

import re
import logging
from typing import List, Optional
from .base import ToolHandler
from services.ollama import ask_ollama

class SmartRouter:
    """智能路由器"""
    
    def __init__(self):
        self.handlers: List[ToolHandler] = []
        self.default_handler: Optional[ToolHandler] = None
    
    def register_handler(self, handler: ToolHandler, is_default: bool = False):
        """注册工具处理器"""
        self.handlers.append(handler)
        if is_default:
            self.default_handler = handler
        logging.info(f"📝 注册工具处理器: {handler.get_tool_name()} - {handler.get_description()}")
    
    def route_with_rules(self, query: str) -> Optional[ToolHandler]:
        """基于规则的路由"""
        for handler in self.handlers:
            if handler != self.default_handler and handler.can_handle(query):
                return handler
        return None
    
    def route_with_ai(self, query: str) -> Optional[ToolHandler]:
        """基于AI模型的智能路由"""
        if len(self.handlers) <= 1:
            return None
            
        # 构建工具列表描述
        tools_desc = ""
        for i, handler in enumerate(self.handlers, 1):
            if handler != self.default_handler:
                tools_desc += f"{i}. {handler.get_tool_name()}: {handler.get_description()}\n"
        
        prompt = f"""
你是一个智能路由器，需要根据用户的问题选择最合适的工具。

可用工具：
{tools_desc}

用户问题：{query}

请按照以下格式回复：
<think>
分析用户问题的意图和需求
</think>
<answer>
选择的工具名称（如果都不合适，回复"general_chat"）
</answer>

回复："""
        
        try:
            result = ask_ollama(prompt)
            answer_match = re.search(r'<answer>(.*?)</answer>', result, re.DOTALL)
            if answer_match:
                selected_tool = answer_match.group(1).strip()
                for handler in self.handlers:
                    if handler.get_tool_name() == selected_tool:
                        logging.info(f"🤖 AI路由选择: {selected_tool}")
                        return handler
        except Exception as e:
            logging.error(f"AI路由失败: {e}")
        
        return None
    
    def route(self, query: str) -> ToolHandler:
        """路由查询到合适的处理器"""
        # 先尝试规则路由
        handler = self.route_with_rules(query)
        if handler:
            logging.info(f"🔀 规则路由选择: {handler.get_tool_name()}")
            return handler
        
        # 再尝试AI路由
        handler = self.route_with_ai(query)
        if handler:
            return handler
        
        # 最后使用默认处理器
        if self.default_handler:
            logging.info(f"🔀 使用默认处理器: {self.default_handler.get_tool_name()}")
            return self.default_handler
        
        # 如果没有默认处理器，返回第一个
        return self.handlers[0] if self.handlers else None 