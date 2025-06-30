from langchain.agents import initialize_agent, AgentType
from tools.weather_tool import weather_tool
from tools.chat_tool import chat_tool
from langchain_community.llms import Ollama

llm = Ollama(
    base_url="http://localhost:11434",
    model="deepseek-r1:7b"
)

tools = [weather_tool, chat_tool]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
) 