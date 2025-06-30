from tools.weather_tool import weather_tool
from tools.chat_tool import chat_tool
from langchain_community.llms import Ollama
import re

llm = Ollama(
    base_url="http://localhost:11434",
    model="deepseek-r1:7b",
    temperature=0.1
)

tools = [weather_tool, chat_tool]

class SimpleAgent:
    """Simplified intelligent agent to avoid complex ReAct format issues"""
    
    def __init__(self, tools, llm):
        self.tools = tools
        self.llm = llm
    
    def invoke(self, inputs):
        query = inputs.get("input", "")
        
        # Intelligent routing: determine intent based on keywords
        if self._is_weather_query(query):
            return self._handle_weather(query)
        else:
            return self._handle_chat(query)
    
    def _is_weather_query(self, query):
        """Determine if it's a weather query"""
        weather_keywords = [
            "weather", "temperature", "temp", "rain", "sunny", "cloudy", "wind", 
            "overcast", "rainy", "snowy", "typhoon", "humidity", "forecast",
            # Chinese keywords for compatibility
            "天气", "气温", "温度", "下雨", "晴天", "阴天", "刮风", 
            "多云", "雨天", "雪天", "台风", "湿度", "风力"
        ]
        return any(keyword in query.lower() for keyword in weather_keywords)
    
    def _handle_weather(self, query):
        """Handle weather queries"""
        city = self._extract_city(query)
        try:
            result = weather_tool.func(city)
            return {
                "output": result,
                "intermediate_steps": [("weather", result)]
            }
        except Exception as e:
            error_msg = f"Weather query failed: {e}"
            return {
                "output": error_msg,
                "intermediate_steps": [("weather", error_msg)]
            }
    
    def _handle_chat(self, query):
        """Handle general conversations"""
        try:
            result = chat_tool.func(query)
            return {
                "output": result,
                "intermediate_steps": [("general_chat", result)]
            }
        except Exception as e:
            error_msg = f"Chat processing failed: {e}"
            return {
                "output": error_msg,
                "intermediate_steps": [("general_chat", error_msg)]
            }
    
    def _extract_city(self, query):
        """Extract city name from query"""
        # Common cities (English and Chinese)
        cities = [
            # English city names
            "beijing", "shanghai", "guangzhou", "shenzhen", "wuhan", "chengdu", 
            "hangzhou", "nanjing", "chongqing", "tianjin", "xian", "suzhou",
            # Chinese city names for compatibility
            "北京", "上海", "广州", "深圳", "武汉", "成都", "杭州", 
            "南京", "重庆", "天津", "西安", "苏州", "长沙", "郑州",
            "青岛", "大连", "宁波", "厦门", "福州", "济南", "昆明",
            "合肥", "太原", "石家庄", "哈尔滨", "长春", "沈阳"
        ]
        
        query_lower = query.lower()
        for city in cities:
            if city in query_lower or city in query:
                return city
        
        # Default to Beijing
        return "Beijing"

# Create simplified agent
agent = SimpleAgent(tools, llm) 