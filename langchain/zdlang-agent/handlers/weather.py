"""
Weather Handler - 天气查询处理器
处理天气相关的查询请求
"""

import logging
from core.base import ToolHandler
from services.weather_api import get_weather
from utils.text_utils import extract_city_with_model, format_weather_data

class WeatherHandler(ToolHandler):
    """天气查询处理器"""
    
    def get_tool_name(self) -> str:
        return "weather"
    
    def get_description(self) -> str:
        return "查询天气信息、气温、降雨等气象数据"
    
    def can_handle(self, query: str) -> bool:
        weather_keywords = ["天气", "气温", "下雨", "晴天", "阴天", "温度", "冷", "热", "气候"]
        return any(keyword in query for keyword in weather_keywords)
    
    def handle(self, query: str) -> dict:
        extraction_result = extract_city_with_model(query)
        city = extraction_result.get("answer", "").strip()
        city_think = extraction_result.get("think", "")
        
        if city and city != "无城市名":
            weather_result = get_weather(city)
            format_result = format_weather_data(city, weather_result)
            format_think = format_result.get("think", "")
            final_answer = format_result.get("answer", "抱歉，处理天气数据时出错。")
            combined_think = f"第一步：提取城市名\n{city_think}\n\n第二步：格式化天气数据\n{format_think}".strip()
            
            logging.info(f"🌤️ 天气问题: {query}")
            logging.info(f"🌤️ 思考过程: {combined_think}")
            logging.info(f"🌤️ 最终答案: {final_answer}")
            return {"think": combined_think, "answer": final_answer}
        else:
            logging.info(f"🌤️ 天气问题: {query}")
            logging.info(f"🌤️ 城市名提取失败: {city_think}")
            return {"think": city_think, "answer": "❌ 无法识别您要查询的城市，请明确指定城市名"} 