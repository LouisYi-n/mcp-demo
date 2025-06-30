from langchain.tools import Tool
import requests
import json

def mcp_weather(city: str) -> str:
    """Call MCP Weather API and return weather information string"""
    try:
        # Handle format errors that LLM might pass, like "city: Beijing" or "城市: Beijing"
        if ":" in city:
            city = city.split(":")[-1].strip()
        city = city.strip()
        resp = requests.get(f"http://localhost:8081/api/weather?cityName={city}", timeout=10)
        if resp.status_code == 200:
            # Check if response content is empty
            if not resp.text.strip():
                return f"Weather service returned empty response, please check service status"
            
            try:
                data = resp.json()
            except json.JSONDecodeError as e:
                return f"Weather service returned non-JSON format data: {resp.text[:100]}"
            
            # Parse fixed format weather data
            if data.get('status') == '1' and 'lives' in data and len(data['lives']) > 0:
                weather_info = data['lives'][0]
                city_name = weather_info.get('city', city)
                weather = weather_info.get('weather', 'Unknown')
                temperature = weather_info.get('temperature', 'Unknown')
                wind_direction = weather_info.get('winddirection', 'Unknown')
                wind_power = weather_info.get('windpower', 'Unknown')
                humidity = weather_info.get('humidity', 'Unknown')
                report_time = weather_info.get('reporttime', 'Unknown')
                
                # Format into natural language
                return f"{city_name} current weather: {weather}, temperature {temperature}°C, {wind_direction} wind {wind_power} level, humidity {humidity}% (updated: {report_time})"
            else:
                return f"Failed to get weather information for {city}, API returned abnormal status: {data.get('info', 'Unknown error')}"
        else:
            return f"Weather service error: HTTP {resp.status_code}, please check if weather service is running normally"
    except requests.exceptions.Timeout:
        return f"Weather service timeout, please try again later"
    except requests.exceptions.ConnectionError:
        return f"Cannot connect to weather service, please check if service is started (localhost:8081)"
    except Exception as e:
        return f"Weather service exception: {e}"

weather_tool = Tool(
    name="weather",
    func=mcp_weather,
    description="Query city weather information, just input city name"
) 
