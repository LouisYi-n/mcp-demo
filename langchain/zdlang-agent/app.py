"""
zdlang-agent 主应用入口文件
智能代理：使用AI路由自动识别意图并调用相应工具
"""

from flask import Flask, request, jsonify, render_template
import logging
from typing import List, Dict

# 导入核心组件
from core.router import SmartRouter
from core.base import ToolHandler

# 导入所有处理器
from handlers.weather import WeatherHandler
from handlers.chat import GeneralChatHandler
from handlers.news import NewsHandler
from handlers.translation import TranslationHandler
from handlers.calculator import CalculatorHandler

# 导入配置
import config

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s'
)

# 创建Flask应用
app = Flask(__name__)

# 初始化智能路由器
router = SmartRouter()

def initialize_handlers():
    """初始化并注册所有工具处理器"""
    # 注册所有工具处理器
    router.register_handler(WeatherHandler())
    router.register_handler(NewsHandler())
    router.register_handler(TranslationHandler()) 
    router.register_handler(CalculatorHandler())
    router.register_handler(GeneralChatHandler(), is_default=True)

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

# ========== 路由定义 ==========

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    """处理用户查询API"""
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'think': '', 'answer': '请输入问题'})
    
    response_dict = process_agent_query(query)
    return jsonify(response_dict)

@app.route('/api/tools', methods=['GET'])
def api_tools():
    """获取所有可用工具列表API"""
    tools = list_available_tools()
    return jsonify(tools)

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "service": "zdlang-agent",
        "handlers_count": len(router.handlers)
    })

def main():
    """主函数"""
    print("🚀 启动 zdlang-agent Web 服务...")
    print("📱 访问地址: http://localhost:5001")
    print("🔧 依赖服务:")
    print(f"   - Ollama: {config.OLLAMA_BASE_URL}")
    print(f"   - 天气API: {config.WEATHER_API_BASE_URL}")
    print()
    
    # 初始化处理器
    initialize_handlers()
    
    # 启动Flask应用
    app.run(
        host=config.FLASK_HOST, 
        port=config.FLASK_PORT, 
        debug=config.FLASK_DEBUG
    )

if __name__ == '__main__':
    main() 