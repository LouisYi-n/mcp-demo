"""
Weather API Service - 天气API服务
负责与天气服务API通信
"""

import requests
import json
import logging

def get_weather(city: str) -> dict:
    """查询指定城市的天气信息"""
    try:
        logging.info(f"DEBUG: 开始查询城市 '{city}' 的天气")
        
        # 尝试不同的参数格式
        test_configs = [
            {"url": f"http://localhost:8081/api/weather?cityName={city}", "method": "GET"},
            {"url": f"http://localhost:8081/api/weather?city={city}", "method": "GET"},
            {"url": f"http://localhost:8081/weather?cityName={city}", "method": "GET"},
            {"url": f"http://localhost:8081/weather?city={city}", "method": "GET"},
            {"url": "http://localhost:8081/api/weather", "method": "POST", "data": {"cityName": city}},
            {"url": "http://localhost:8081/api/weather", "method": "POST", "data": {"city": city}},
        ]
        
        for i, config in enumerate(test_configs, 1):
            try:
                logging.info(f"DEBUG: 尝试配置 {i}: {config}")
                
                if config["method"] == "GET":
                    resp = requests.get(config["url"], timeout=10)
                else:  # POST
                    resp = requests.post(config["url"], json=config["data"], timeout=10)
                
                logging.info(f"DEBUG: 状态码: {resp.status_code}")
                logging.info(f"DEBUG: 响应头: {dict(resp.headers)}")
                logging.info(f"DEBUG: 响应内容: {resp.text}")
                
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        logging.info(f"DEBUG: 成功获取天气数据: {data}")
                        
                        # 检查API返回的错误状态
                        if isinstance(data, dict):
                            # 检查常见的错误状态
                            if (data.get("status") == "0" and 
                                ("INVALID_PARAMS" in str(data.get("info", "")) or 
                                 "infocode" in data)):
                                logging.info(f"DEBUG: 检测到城市不存在或参数无效: {data}")
                                return {"city_not_found": True, "original_data": data, "city": city}
                            
                            # 检查其他可能的错误格式
                            if (data.get("error") or 
                                data.get("status") == "error" or
                                "error" in str(data.get("message", "")).lower()):
                                logging.info(f"DEBUG: 检测到API错误: {data}")
                                return {"api_error": True, "original_data": data, "city": city}
                        
                        return data
                    except json.JSONDecodeError:
                        logging.info(f"DEBUG: 响应不是JSON格式: {resp.text}")
                        return {"weather": resp.text}
                else:
                    logging.info(f"DEBUG: HTTP错误 {resp.status_code}: {resp.text}")
                    
            except Exception as e:
                logging.info(f"DEBUG: 配置 {i} 失败: {e}")
                continue
        
        # 如果所有配置都失败，返回错误信息
        error_msg = f"所有天气API配置都失败，城市: {city}"
        logging.info(f"DEBUG: {error_msg}")
        return {"error": error_msg}
        
    except Exception as e:
        error_msg = f"天气服务异常: {e}"
        logging.info(f"DEBUG: {error_msg}")
        return {"error": error_msg} 