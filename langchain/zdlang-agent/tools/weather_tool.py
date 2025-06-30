from langchain.tools import Tool
import requests
import json

def mcp_weather(city: str) -> str:
    """调用 MCP 天气 API，返回天气信息字符串"""
    try:
        # 处理LLM可能传入的格式错误参数，如 "city: 北京" 或 "城市: 北京"
        if ":" in city:
            city = city.split(":")[-1].strip()
        city = city.strip()
        resp = requests.get(f"http://localhost:8081/api/weather?cityName={city}", timeout=10)
        if resp.status_code == 200:
            # 检查响应内容是否为空
            if not resp.text.strip():
                return f"天气服务返回空响应，请检查服务状态"
            
            try:
                data = resp.json()
            except json.JSONDecodeError as e:
                return f"天气服务返回非JSON格式数据：{resp.text[:100]}"
            
            # 解析固定格式的天气数据
            if data.get('status') == '1' and 'lives' in data and len(data['lives']) > 0:
                weather_info = data['lives'][0]
                city_name = weather_info.get('city', city)
                weather = weather_info.get('weather', '未知')
                temperature = weather_info.get('temperature', '未知')
                wind_direction = weather_info.get('winddirection', '未知')
                wind_power = weather_info.get('windpower', '未知')
                humidity = weather_info.get('humidity', '未知')
                report_time = weather_info.get('reporttime', '未知')
                
                # 格式化成自然语言
                return f"{city_name}当前天气：{weather}，温度{temperature}°C，{wind_direction}风{wind_power}级，湿度{humidity}%（更新时间：{report_time}）"
            else:
                return f"获取{city}天气信息失败，API返回状态异常：{data.get('info', '未知错误')}"
        else:
            return f"天气服务错误: HTTP {resp.status_code}，请检查天气服务是否正常运行"
    except requests.exceptions.Timeout:
        return f"天气服务超时，请稍后重试"
    except requests.exceptions.ConnectionError:
        return f"无法连接天气服务，请检查服务是否启动（localhost:8081）"
    except Exception as e:
        return f"天气服务异常: {e}"

weather_tool = Tool(
    name="weather",
    func=mcp_weather,
    description="查询城市天气信息，输入城市名即可"
) 
