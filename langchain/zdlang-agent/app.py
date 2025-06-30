"""
zdlang-agent 主应用入口文件
智能代理：使用AI路由自动识别意图并调用相应工具
"""

from flask import Flask, request, jsonify, render_template
import logging
from typing import List, Dict

# 导入配置
import config

# 导入 LangChain Agent
from agent import agent

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s'
)

# 创建Flask应用
app = Flask(__name__)

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
        return jsonify({'result': '请输入问题'})
    
    result = agent.invoke({"input": query})
    
    # 解析工具调用过程
    tool_calls = []
    answer = ""
    
    if isinstance(result, dict):
        # 提取工具调用信息
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                tool_name = step[0]  # 现在是简单的字符串
                observation = step[1]
                
                # 只有调用外部服务的工具才显示调用信息
                if tool_name == 'weather':
                    tool_calls.append(f"🔧 我调用了 weather MCP，结果是：{observation}")
                # general_chat 工具不显示调用信息，因为只是调用了大模型
                # 其他工具可以根据需要添加
        answer = result.get("output", str(result))
    else:
        answer = str(result)
    
    return jsonify({
        'result': answer,
        'tool_calls': tool_calls
    })

@app.route('/api/tools', methods=['GET'])
def api_tools():
    """获取所有可用工具列表API"""
    # 返回工具的 name 和 description
    if hasattr(agent, 'tools'):
        tools = agent.tools
    elif hasattr(agent, 'base_agent') and hasattr(agent.base_agent, 'tools'):
        tools = agent.base_agent.tools
    else:
        # 导入工具作为备选
        from tools.weather_tool import weather_tool
        from tools.chat_tool import chat_tool
        tools = [weather_tool, chat_tool]
    
    return jsonify({'tools': [
        {'name': tool.name, 'description': tool.description}
        for tool in tools
    ]})

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "healthy",
        "service": "zdlang-agent"
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    result = agent.invoke({"input": query})
    if isinstance(result, dict) and "output" in result:
        result = result["output"]
    return jsonify({"result": result})

def main():
    """主函数"""
    print("🚀 启动 zdlang-agent Web 服务...")
    print("📱 访问地址: http://localhost:5001")
    print("🔧 依赖服务:")
    print(f"   - Ollama: {config.OLLAMA_BASE_URL}")
    print(f"   - 天气API: {config.WEATHER_API_BASE_URL}")
    print()
    
    # 直接启动 Flask
    app.run(
        host=config.FLASK_HOST, 
        port=config.FLASK_PORT, 
        debug=config.FLASK_DEBUG
    )

if __name__ == '__main__':
    main() 