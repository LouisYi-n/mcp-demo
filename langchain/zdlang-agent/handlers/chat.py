"""
General Chat Handler - 通用对话处理器
处理一般性的对话和问答请求
"""

import re
import logging
from core.base import ToolHandler
from services.ollama import ask_ollama
from utils.text_utils import clean_answer

class GeneralChatHandler(ToolHandler):
    """通用对话处理器"""
    
    def get_tool_name(self) -> str:
        return "general_chat"
    
    def get_description(self) -> str:
        return "通用对话、问答、知识查询等"
    
    def can_handle(self, query: str) -> bool:
        return True  # 默认处理器，总是返回True
    
    def handle(self, query: str) -> dict:
        logging.info(f"🤖 普通对话请求: {query}")
        prompt = f"""
请回答以下问题：

问题：{query}

请按照以下格式回复：
<think>
在这里进行思考和分析过程
</think>
<answer>
在这里提供最终答案
</answer>

回复："""
        try:
            result = ask_ollama(prompt)
            think_match = re.search(r'<think>(.*?)</think>', result, re.DOTALL)
            answer_match = re.search(r'<answer>(.*?)</answer>', result, re.DOTALL)
            
            think_content = think_match.group(1).strip() if think_match else ""
            
            # 如果找到了answer标签，使用其内容；否则使用整个结果并清理标签
            if answer_match:
                answer_content = answer_match.group(1).strip()
            else:
                answer_content = result.strip()
            
            # 清理answer中可能残留的标签
            answer_content = clean_answer(answer_content)
            
            logging.info(f"🤖 模型思考: {think_content}")
            logging.info(f"🤖 最终答案: {answer_content}")
            return {"think": think_content, "answer": answer_content}
        except Exception as e:
            logging.error(f"🤖 普通对话异常: {e}")
            return {"think": "回答失败", "answer": f"回答失败: {e}"} 