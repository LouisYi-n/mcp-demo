from langchain.tools import Tool
import requests

def mcp_weather(city: str) -> str:
    """调用 MCP 天气 API，返回天气信息字符串"""
    try:
        resp = requests.get(f"http://localhost:8081/api/weather?cityName={city}", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            # 简单格式化
            if 'weather' in data:
                return f"{city}天气：{data['weather']}，温度：{data.get('temperature', '未知')}"
            return str(data)
        else:
            return f"天气服务错误: {resp.status_code}"
    except Exception as e:
        return f"天气服务异常: {e}"

weather_tool = Tool(
    name="weather",
    func=mcp_weather,
    description="查询城市天气信息，输入城市名即可"
) 