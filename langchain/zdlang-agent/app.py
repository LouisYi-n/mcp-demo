"""
zdlang-agent Main Application Entry
Intelligent Agent: Automatically identifies user intent and calls appropriate tools using AI routing
"""

from flask import Flask, request, jsonify, render_template
import logging
from typing import List, Dict

# Import configuration
import config

# Import LangChain Agent
from agent import agent

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(message)s'
)

# Create Flask application
app = Flask(__name__)

# ========== Route Definitions ==========

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    """Handle user query API"""
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'result': 'Please enter a question'})
    
    result = agent.invoke({"input": query})
    
    # Parse tool calling process
    tool_calls = []
    answer = ""
    
    if isinstance(result, dict):
        # Extract tool calling information
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                tool_name = step[0]  # Now it's a simple string
                observation = step[1]
                
                # Only show calling information for external service tools
                if tool_name == 'weather':
                    tool_calls.append(f"🔧 I called weather MCP, result: {observation}")
                # general_chat tool doesn't show calling info, as it only calls the LLM
                # Other tools can be added as needed
        answer = result.get("output", str(result))
    else:
        answer = str(result)
    
    return jsonify({
        'result': answer,
        'tool_calls': tool_calls
    })

@app.route('/api/tools', methods=['GET'])
def api_tools():
    """Get all available tools list API"""
    # Return tool name and description
    if hasattr(agent, 'tools'):
        tools = agent.tools
    elif hasattr(agent, 'base_agent') and hasattr(agent.base_agent, 'tools'):
        tools = agent.base_agent.tools
    else:
        # Import tools as fallback
        from tools.weather_tool import weather_tool
        from tools.chat_tool import chat_tool
        tools = [weather_tool, chat_tool]
    
    return jsonify({'tools': [
        {'name': tool.name, 'description': tool.description}
        for tool in tools
    ]})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
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
    """Main function"""
    print("🚀 Starting zdlang-agent Web Service...")
    print("📱 Access URL: http://localhost:5001")
    print("🔧 Dependent Services:")
    print(f"   - Ollama: {config.OLLAMA_BASE_URL}")
    print(f"   - Weather API: {config.WEATHER_API_BASE_URL}")
    print()
    
    # Start Flask directly
    app.run(
        host=config.FLASK_HOST, 
        port=config.FLASK_PORT, 
        debug=config.FLASK_DEBUG
    )

if __name__ == '__main__':
    main() 