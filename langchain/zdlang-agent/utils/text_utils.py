"""
Text Utils - 文本处理工具
包含文本清理、城市提取、天气数据格式化等功能
"""

import re
import logging
from services.ollama import ask_ollama

def clean_answer(answer: str) -> str:
    """移除answer中的所有XML标签，只保留最终回复"""
    # 移除<think>...</think>片段
    answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL)
    # 移除<answer>和</answer>标签
    answer = re.sub(r'</?answer>', '', answer, flags=re.IGNORECASE)
    # 移除其他可能的XML标签
    answer = re.sub(r'<[^>]+>', '', answer)
    return answer.strip()

def extract_city_with_model(query: str) -> dict:
    """使用模型分析问题并提取城市名"""
    prompt = f"""
请分析以下问题，如果是在询问天气，请提取出城市名。如果问题中没有城市名或不是询问天气，请回复"无城市名"。

问题：{query}

请按照以下格式回复：
<think>
在这里进行思考和分析过程
</think>
<answer>
最终答案（只包含城市名或"无城市名"）
</answer>

示例：
- 问题："北京天气怎么样？" 
<think>
用户询问北京的天气，问题中包含城市名"北京"，这是一个天气相关问题。
</think>
<answer>
北京
</answer>

- 问题："今天天气如何"
<think>
用户询问今天的天气，但没有指定具体城市，无法提取城市名。
</think>
<answer>
无城市名
</answer>

回复："""
    
    try:
        result = ask_ollama(prompt)
        think_match = re.search(r'<think>(.*?)</think>', result, re.DOTALL)
        answer_match = re.search(r'<answer>(.*?)</answer>', result, re.DOTALL)
        think_content = think_match.group(1).strip() if think_match else ""
        answer_content = answer_match.group(1).strip() if answer_match else ""
        answer_content = clean_answer(answer_content)
        if answer_content == "无城市名" or not answer_content:
            return {"think": think_content, "answer": "无城市名"}
        return {"think": think_content, "answer": answer_content}
    except Exception as e:
        return {"think": "模型提取城市名失败", "answer": "无法提取城市名"}

def format_weather_data(city: str, weather_data: dict) -> dict:
    """使用模型格式化天气数据"""
    # 检查是否是城市不存在的情况
    if weather_data.get("city_not_found"):
        return {
            "think": f"检测到城市'{city}'不存在或拼写错误，需要给用户友好的提示",
            "answer": f"❌ 抱歉，无法找到城市「{city}」的天气信息。\n\n可能的原因：\n• 城市名称拼写错误\n• 该城市不在天气服务数据库中\n\n💡 建议：\n• 请检查城市名称是否正确\n• 尝试使用城市的标准中文名称\n• 如果是县级市，可以尝试使用所属地级市名称\n\n例如：北京、上海、广州、深圳、杭州、哈尔滨等"
        }
    
    # 检查是否是API错误
    if weather_data.get("api_error"):
        return {
            "think": f"检测到天气API返回错误，城市'{city}'可能不支持或服务异常",
            "answer": f"⚠️ 获取城市「{city}」的天气信息时出现问题。\n\n可能的原因：\n• 天气服务暂时不可用\n• 该城市暂不支持天气查询\n\n请稍后重试或更换其他城市查询。"
        }
    
    # 检查是否有通用错误
    if weather_data.get("error"):
        return {
            "think": f"天气服务出现错误：{weather_data.get('error')}",
            "answer": f"⚠️ 天气服务暂时不可用：{weather_data.get('error')}\n\n请稍后重试。"
        }
    
    # 正常的天气数据格式化
    prompt = f"""
请将以下天气数据格式化为用户友好的中文回复：

城市：{city}
天气数据：{weather_data}

请按照以下格式回复：
<think>
在这里分析天气数据，思考如何用友好的语言描述
</think>
<answer>
在这里提供最终的用户友好回复，包括问候语、天气描述等
</answer>

回复："""
    
    try:
        result = ask_ollama(prompt)
        think_match = re.search(r'<think>(.*?)</think>', result, re.DOTALL)
        answer_match = re.search(r'<answer>(.*?)</answer>', result, re.DOTALL)
        think_content = think_match.group(1).strip() if think_match else ""
        answer_content = answer_match.group(1).strip() if answer_match else result.strip()
        answer_content = clean_answer(answer_content)
        return {"think": think_content, "answer": answer_content}
    except Exception as e:
        return {"think": "格式化失败", "answer": f"格式化失败: {e}"} 