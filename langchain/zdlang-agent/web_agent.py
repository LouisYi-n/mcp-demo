import requests
import json
from flask import Flask, request, jsonify, render_template_string
import re
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

# 天气查询工具
def get_weather(city: str):
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

# 直接调用 Ollama API
def ask_ollama(prompt: str):
    """直接调用 Ollama API 使用 deepseek-r1-7b 模型"""
    try:
        data = {
            "model": "deepseek-r1:7b",
            "prompt": prompt,
            "stream": False
        }
        
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if resp.status_code == 200:
            result = resp.json()
            return result.get("response", "未获取到模型回复")
        else:
            return f"Ollama 服务错误: {resp.status_code}"
    except Exception as e:
        return f"Ollama 服务异常: {e}"

def clean_answer(answer):
    """移除answer中的所有XML标签，只保留最终回复"""
    # 移除<think>...</think>片段
    answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL)
    # 移除<answer>和</answer>标签
    answer = re.sub(r'</?answer>', '', answer, flags=re.IGNORECASE)
    # 移除其他可能的XML标签
    answer = re.sub(r'<[^>]+>', '', answer)
    return answer.strip()

# 使用模型提取城市名
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

# 使用模型格式化天气数据
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

# 智能路由器和工具处理器基类
class ToolHandler(ABC):
    """工具处理器基类"""
    
    @abstractmethod
    def get_tool_name(self) -> str:
        """返回工具名称"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """返回工具描述，用于智能路由"""
        pass
    
    @abstractmethod
    def can_handle(self, query: str) -> bool:
        """简单规则判断是否能处理该查询"""
        pass
    
    @abstractmethod
    def handle(self, query: str) -> dict:
        """处理查询并返回结果"""
        pass

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

class NewsHandler(ToolHandler):
    """新闻查询处理器 - 示例"""
    
    def get_tool_name(self) -> str:
        return "news"
    
    def get_description(self) -> str:
        return "查询最新新闻、时事资讯、热点事件"
    
    def can_handle(self, query: str) -> bool:
        news_keywords = ["新闻", "资讯", "热点", "最新", "今日", "头条", "报道"]
        return any(keyword in query for keyword in news_keywords)
    
    def handle(self, query: str) -> dict:
        # TODO: 实现具体的新闻查询逻辑
        logging.info(f"📰 新闻查询请求: {query}")
        return {
            "think": "识别为新闻查询请求，但新闻服务尚未实现",
            "answer": "📰 新闻查询功能开发中，敬请期待！\n\n如需查询具体信息，请尝试其他问题。"
        }

class TranslationHandler(ToolHandler):
    """翻译处理器 - 示例"""
    
    def get_tool_name(self) -> str:
        return "translation"
    
    def get_description(self) -> str:
        return "文本翻译、语言转换服务"
    
    def can_handle(self, query: str) -> bool:
        translation_keywords = ["翻译", "translate", "英文", "中文", "日文", "韩文", "法文", "德文"]
        return any(keyword in query for keyword in translation_keywords)
    
    def handle(self, query: str) -> dict:
        # TODO: 实现具体的翻译逻辑
        logging.info(f"🌐 翻译请求: {query}")
        return {
            "think": "识别为翻译请求，但翻译服务尚未实现",
            "answer": "🌐 翻译功能开发中，敬请期待！\n\n如需翻译，请尝试使用在线翻译工具。"
        }

class CalculatorHandler(ToolHandler):
    """计算器处理器 - 示例"""
    
    def get_tool_name(self) -> str:
        return "calculator"
    
    def get_description(self) -> str:
        return "数学计算、公式运算"
    
    def can_handle(self, query: str) -> bool:
        calc_keywords = ["计算", "算", "等于", "+", "-", "*", "/", "=", "数学"]
        math_patterns = [r'\d+\s*[+\-*/]\s*\d+', r'计算.*\d+']
        
        # 检查关键词
        if any(keyword in query for keyword in calc_keywords):
            return True
        
        # 检查数学表达式模式
        import re
        return any(re.search(pattern, query) for pattern in math_patterns)
    
    def handle(self, query: str) -> dict:
        # TODO: 实现具体的计算逻辑
        logging.info(f"🧮 计算请求: {query}")
        return {
            "think": "识别为计算请求，但计算服务尚未实现",
            "answer": "🧮 计算功能开发中，敬请期待！\n\n如需计算，请尝试使用计算器应用。"
        }

class GeneralChatHandler(ToolHandler):
    """通用对话处理器"""
    
    def get_tool_name(self) -> str:
        return "general_chat"
    
    def get_description(self) -> str:
        return "通用对话、问答、知识查询等"
    
    def can_handle(self, query: str) -> bool:
        return True  # 默认处理器，总是返回True
    
    def handle(self, query: str) -> dict:
        logging.info(f"🤖 普通对话请求: {query}")
        prompt = f"""
请回答以下问题：

问题：{query}

请按照以下格式回复：
<think>
在这里进行思考和分析过程
</think>
<answer>
在这里提供最终答案
</answer>

回复："""
        try:
            result = ask_ollama(prompt)
            think_match = re.search(r'<think>(.*?)</think>', result, re.DOTALL)
            answer_match = re.search(r'<answer>(.*?)</answer>', result, re.DOTALL)
            
            think_content = think_match.group(1).strip() if think_match else ""
            
            # 如果找到了answer标签，使用其内容；否则使用整个结果并清理标签
            if answer_match:
                answer_content = answer_match.group(1).strip()
            else:
                answer_content = result.strip()
            
            # 清理answer中可能残留的标签
            answer_content = clean_answer(answer_content)
            
            logging.info(f"🤖 模型思考: {think_content}")
            logging.info(f"🤖 最终答案: {answer_content}")
            return {"think": think_content, "answer": answer_content}
        except Exception as e:
            logging.error(f"🤖 普通对话异常: {e}")
            return {"think": "回答失败", "answer": f"回答失败: {e}"}

class SmartRouter:
    """智能路由器"""
    
    def __init__(self):
        self.handlers: List[ToolHandler] = []
        self.default_handler: Optional[ToolHandler] = None
    
    def register_handler(self, handler: ToolHandler, is_default: bool = False):
        """注册工具处理器"""
        self.handlers.append(handler)
        if is_default:
            self.default_handler = handler
        logging.info(f"📝 注册工具处理器: {handler.get_tool_name()} - {handler.get_description()}")
    
    def route_with_rules(self, query: str) -> Optional[ToolHandler]:
        """基于规则的路由"""
        for handler in self.handlers:
            if handler != self.default_handler and handler.can_handle(query):
                return handler
        return None
    
    def route_with_ai(self, query: str) -> Optional[ToolHandler]:
        """基于AI模型的智能路由"""
        if len(self.handlers) <= 1:
            return None
            
        # 构建工具列表描述
        tools_desc = ""
        for i, handler in enumerate(self.handlers, 1):
            if handler != self.default_handler:
                tools_desc += f"{i}. {handler.get_tool_name()}: {handler.get_description()}\n"
        
        prompt = f"""
你是一个智能路由器，需要根据用户的问题选择最合适的工具。

可用工具：
{tools_desc}

用户问题：{query}

请按照以下格式回复：
<think>
分析用户问题的意图和需求
</think>
<answer>
选择的工具名称（如果都不合适，回复"general_chat"）
</answer>

回复："""
        
        try:
            result = ask_ollama(prompt)
            answer_match = re.search(r'<answer>(.*?)</answer>', result, re.DOTALL)
            if answer_match:
                selected_tool = answer_match.group(1).strip()
                for handler in self.handlers:
                    if handler.get_tool_name() == selected_tool:
                        logging.info(f"�� AI路由选择: {selected_tool}")
                        return handler
        except Exception as e:
            logging.error(f"AI路由失败: {e}")
        
        return None
    
    def route(self, query: str) -> ToolHandler:
        """路由查询到合适的处理器"""
        # 先尝试规则路由
        handler = self.route_with_rules(query)
        if handler:
            logging.info(f"🔀 规则路由选择: {handler.get_tool_name()}")
            return handler
        
        # 再尝试AI路由
        handler = self.route_with_ai(query)
        if handler:
            return handler
        
        # 最后使用默认处理器
        if self.default_handler:
            logging.info(f"🔀 使用默认处理器: {self.default_handler.get_tool_name()}")
            return self.default_handler
        
        # 如果没有默认处理器，返回第一个
        return self.handlers[0] if self.handlers else None

# 初始化智能路由器
router = SmartRouter()

# 注册所有工具处理器
router.register_handler(WeatherHandler())
router.register_handler(NewsHandler())
router.register_handler(TranslationHandler()) 
router.register_handler(CalculatorHandler())
router.register_handler(GeneralChatHandler(), is_default=True)

# 重构后的主要处理函数
def process_agent_query(query: str) -> dict:
    """处理用户查询，使用智能路由分发到合适的工具处理器"""
    try:
        handler = router.route(query)
        if handler:
            return handler.handle(query)
        else:
            return {"think": "未找到合适的处理器", "answer": "抱歉，无法处理您的请求"}
    except Exception as e:
        logging.error(f"查询处理异常: {e}")
        return {"think": f"处理异常: {e}", "answer": "处理请求时发生错误，请稍后重试"}

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>zdlang-agent</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 20px; }
        .header h1 { color: #333; margin-bottom: 10px; }
        .header p { color: #666; }
        .chat-box { border: 1px solid #ddd; height: 500px; overflow-y: auto; padding: 15px; margin-bottom: 15px; border-radius: 8px; background: #fafafa; }
        .input-area { display: flex; gap: 10px; }
        #query { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
        button { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
        button:hover { background: #0056b3; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        .user-msg { background: #e3f2fd; padding: 10px; margin: 8px 0; border-radius: 8px; border-left: 4px solid #2196f3; }
        .agent-msg {
            background: #f1f8e9;
            padding: 10px 15px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
            white-space: pre-wrap; /* 保持换行和空格 */
        }
        .think-msg {
            color: #6c757d; /* 灰色字体 */
            background: #f8f9fa; /* 更浅的背景 */
            border-left: 4px solid #adb5bd; /* 灰色边框 */
            font-size: 0.9em; /* 字体稍小 */
            margin-bottom: 5px; /* 与最终回复的间距 */
        }
        .loading { text-align: center; color: #666; font-style: italic; }
        .error { background: #ffebee; border-left: 4px solid #f44336; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 zdlang-agent</h1>
            <p>智能代理：使用AI路由自动识别意图并调用相应工具</p>
            <div id="toolsList" style="margin-top: 10px; font-size: 12px; color: #666;"></div>
        </div>
        
        <div class="chat-box" id="chatBox">
            <div class="agent-msg">👋 欢迎使用 zdlang-agent！请输入您的问题。</div>
        </div>
        
        <div class="input-area">
            <input type="text" id="query" placeholder="输入您的问题，例如：北京天气怎么样？" onkeypress="if(event.keyCode==13) sendQuery()">
            <button onclick="sendQuery()" id="sendBtn">发送</button>
        </div>
    </div>

    <script>
        // 加载可用工具列表
        function loadTools() {
            fetch('/api/tools')
                .then(response => response.json())
                .then(tools => {
                    const toolsList = document.getElementById('toolsList');
                    const toolNames = tools.map(tool => {
                        const icon = tool.is_default ? '🤖' : getToolIcon(tool.name);
                        return `${icon} ${tool.description}`;
                    });
                    toolsList.innerHTML = `可用工具: ${toolNames.join(' | ')}`;
                })
                .catch(error => console.error('加载工具失败:', error));
        }
        
        function getToolIcon(toolName) {
            const icons = {
                'weather': '🌤️',
                'news': '📰',
                'translation': '🌐',
                'calculator': '🧮',
                'general_chat': '🤖'
            };
            return icons[toolName] || '🔧';
        }
        
        // 页面加载时获取工具列表
        document.addEventListener('DOMContentLoaded', loadTools);
        
        function sendQuery() {
            const query = document.getElementById('query').value.trim();
            const sendBtn = document.getElementById('sendBtn');
            if (!query) return;
            sendBtn.disabled = true;
            document.getElementById('query').disabled = true;
            addMessage(query, 'user-msg');
            document.getElementById('query').value = '';
            const loadingId = addMessage('正在思考中...', 'agent-msg loading');
            fetch('/api/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: query})
            })
            .then(response => response.json())
            .then(data => {
                removeMessage(loadingId);
                if (data.think) {
                    addMessage('🤔 ' + data.think, 'agent-msg think-msg');
                }
                if (data.answer) {
                    addMessage('💬 ' + data.answer, 'agent-msg');
                } else if (!data.think) {
                    addMessage('抱歉，我没有得到回复。', 'agent-msg error');
                }
            })
            .catch(error => {
                removeMessage(loadingId);
                addMessage('发生错误: ' + error, 'agent-msg error');
            })
            .finally(() => {
                sendBtn.disabled = false;
                document.getElementById('query').disabled = false;
                document.getElementById('query').focus();
            });
        }
        function addMessage(text, className) {
            const chatBox = document.getElementById('chatBox');
            const div = document.createElement('div');
            if (className.includes('user-msg')) {
                div.textContent = '你: ' + text;
            } else {
                div.textContent = text;
            }
            div.className = className;
            div.id = 'msg-' + Date.now();
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
            return div.id;
        }
        function removeMessage(messageId) {
            const element = document.getElementById(messageId);
            if (element) {
                element.remove();
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'think': '', 'answer': '请输入问题'})
    response_dict = process_agent_query(query)
    return jsonify(response_dict)

@app.route('/api/tools', methods=['GET'])
def api_tools():
    """获取所有可用工具列表"""
    tools = list_available_tools()
    return jsonify(tools)

# ========== 工具管理API ==========
def list_available_tools() -> List[Dict[str, str]]:
    """列出所有可用的工具"""
    tools = []
    for handler in router.handlers:
        tools.append({
            "name": handler.get_tool_name(),
            "description": handler.get_description(),
            "is_default": handler == router.default_handler
        })
    return tools

if __name__ == '__main__':
    print("🚀 启动 zdlang-agent Web 服务...")
    print("📱 访问地址: http://localhost:5000")
    print("🔧 依赖服务:")
    print("   - Ollama: http://localhost:11434")
    print("   - mcp-server: http://localhost:8081")
    app.run(host='0.0.0.0', port=5000, debug=True) 