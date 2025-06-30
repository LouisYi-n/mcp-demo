from langchain.tools import Tool
from langchain_community.llms import Ollama

llm = Ollama(
    base_url="http://localhost:11434",
    model="deepseek-r1:7b"
)

def general_chat(query: str) -> str:
    return llm(query)

chat_tool = Tool(
    name="general_chat",
    func=general_chat,
    description="通用对话、知识问答"
) 