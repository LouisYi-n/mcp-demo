from langchain.tools import Tool
from langchain_community.llms import Ollama
import re
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = Ollama(
    base_url="http://localhost:11434",
    model="deepseek-r1:7b",
    temperature=0.7,
    verbose=True  # 启用详细日志
)

def general_chat(query: str) -> str:
    """通用对话工具，处理一般问题和聊天"""
    try:
        logger.info(f"调用 Ollama 模型处理查询: {query[:50]}...")
        
        # 使用现代的 invoke 方法
        response = llm.invoke(query)
        
        # 清理响应内容，移除 <think> 标签
        cleaned_response = clean_response(response)
        
        logger.info(f"Ollama 响应完成，长度: {len(cleaned_response)} 字符")
        return cleaned_response
        
    except Exception as e:
        error_msg = f"对话处理失败: {e}"
        logger.error(error_msg)
        return error_msg

def clean_response(response: str) -> str:
    """清理响应内容，移除think标签和多余的空白"""
    if not response:
        return "抱歉，我没有生成回复。"
    
    # 移除 <think> 标签及其内容
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    
    # 移除多余的空白行
    response = re.sub(r'\n\s*\n', '\n\n', response)
    
    # 去除首尾空白
    response = response.strip()
    
    # 如果清理后为空，返回默认消息
    if not response:
        return "我理解了您的问题，但暂时无法给出合适的回答。请尝试换个方式提问。"
    
    return response

chat_tool = Tool(
    name="general_chat",
    func=general_chat,
    description="通用对话、知识问答、讲笑话等"
) 