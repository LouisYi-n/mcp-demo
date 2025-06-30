# ZDLang Agent - Intelligent Multi-Tool Agent System

A sophisticated intelligent agent system built with LangChain that automatically routes between local LLM services and MCP (Model Context Protocol) weather services. The system provides seamless integration between conversational AI and weather data retrieval through an intuitive web interface.

## 🌟 Features

- **Intelligent Routing**: Automatically detects user intent and routes to appropriate tools
- **Dual-Language Support**: Supports both English and Chinese queries
- **Weather Integration**: Real-time weather data via MCP weather service
- **Local LLM**: Powered by deepseek-r1-7b model through Ollama
- **Web Interface**: Clean, modern web UI for easy interaction
- **RESTful API**: Complete API endpoints for programmatic access
- **Tool Transparency**: Shows which tools are being used during processing

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │────│  Flask Web API  │────│  SimpleAgent    │
│   (index.html)  │    │    (app.py)     │    │   (agent.py)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │ Intent Router   │
                                              │ (Keyword Match) │
                                              └─────────────────┘
                                                       │
                                    ┌──────────────────┼──────────────────┐
                                    ▼                  ▼                  ▼
                           ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
                           │  Weather Tool   │ │   Chat Tool     │ │  External APIs  │
                           │(weather_tool.py)│ │ (chat_tool.py)  │ │                 │
                           └─────────────────┘ └─────────────────┘ └─────────────────┘
                                    │                  │
                                    ▼                  ▼
                           ┌─────────────────┐ ┌─────────────────┐
                           │ MCP Weather API │ │  Ollama LLM     │
                           │ (localhost:8081)│ │(localhost:11434)│
                           └─────────────────┘ └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Ollama with deepseek-r1-7b model
- MCP Weather Service running on port 8081
- Node.js (for MCP service)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd zdlang-agent
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ollama pull deepseek-r1:7b
   ```

4. **Start MCP Weather Service**
   ```bash
   # In a separate terminal
   cd mcp-weather-service
   npm start
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the web interface**
   Open your browser and navigate to: `http://localhost:5001`

## 📋 API Endpoints

### Health Check
```http
GET /health
```
Returns system health status.

### Get Available Tools
```http
GET /api/tools
```
Returns list of available tools with descriptions.

### Query Processing
```http
POST /api/query
Content-Type: application/json

{
  "query": "What's the weather in Beijing?"
}
```

**Response:**
```json
{
  "success": true,
  "result": "Beijing current weather: overcast, temperature 28°C, southeast wind ≤3 level, humidity 78%",
  "intermediate_steps": [["weather", "Weather data retrieved successfully"]],
  "query": "What's the weather in Beijing?"
}
```

## 🛠️ Project Structure

```
zdlang-agent/
├── app.py                 # Flask web server and API endpoints
├── agent.py              # SimpleAgent implementation
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── tools/
│   ├── __init__.py
│   ├── weather_tool.py   # Weather query tool
│   └── chat_tool.py      # General conversation tool
├── templates/
│   └── index.html        # Web interface
└── core/
    └── __init__.py
```

## 🔧 Configuration

Edit `config.py` to customize:

- **Flask Settings**: Port, debug mode, host configuration
- **Ollama Settings**: Model name, API endpoint
- **MCP Settings**: Weather service URL and timeout
- **Agent Settings**: Max iterations, execution timeout

```python
# Example configuration
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 5001,
    'debug': True
}

OLLAMA_CONFIG = {
    'base_url': 'http://localhost:11434',
    'model': 'deepseek-r1:7b'
}
```

## 💡 Usage Examples

### Weather Queries
- "What's the weather in Shanghai?"
- "上海天气怎么样？"
- "Tell me about Beijing's weather"
- "北京现在下雨吗？"

### General Conversation
- "Tell me a joke"
- "What is artificial intelligence?"
- "Explain quantum computing"
- "How do neural networks work?"

## 🔍 How It Works

1. **Intent Recognition**: The SimpleAgent analyzes user queries using keyword matching
2. **Tool Selection**: Based on detected intent, routes to appropriate tool:
   - Weather keywords → Weather Tool → MCP Weather API
   - Other queries → Chat Tool → Ollama LLM
3. **Response Processing**: Tools process requests and return formatted responses
4. **Result Delivery**: Final results are sent back through the API to the frontend

## 🌤️ Weather Tool Features

- **Multi-language Support**: Recognizes weather queries in English and Chinese
- **City Recognition**: Supports major cities in both languages
- **Data Processing**: Directly parses weather API responses for optimal performance
- **Error Handling**: Comprehensive error handling for API failures

**Supported Weather Keywords:**
- English: weather, temperature, rain, sunny, cloudy, wind
- Chinese: 天气, 气温, 温度, 下雨, 晴天, 阴天, 刮风

## 💬 Chat Tool Features

- **LLM Integration**: Powered by deepseek-r1-7b through Ollama
- **Response Cleaning**: Removes internal thinking tags for clean output
- **Error Recovery**: Handles LLM failures gracefully
- **Logging**: Comprehensive logging for debugging

## 🎯 Key Design Decisions

### Why SimpleAgent?
- **Reliability**: Avoids complex ReAct format parsing issues
- **Performance**: Direct keyword matching is faster than LLM-based routing
- **Maintainability**: Easier to debug and extend
- **Predictability**: Consistent behavior across different query types

### Tool Architecture Benefits
- **Modularity**: Easy to add new tools
- **Isolation**: Tool failures don't affect the entire system
- **Flexibility**: Each tool can have its own processing logic
- **Scalability**: Can easily integrate additional external services

## 🚨 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   - Ensure Ollama service is running: `ollama serve`
   - Check if model is installed: `ollama list`

2. **MCP Weather Service Unavailable**
   - Verify MCP service is running on port 8081
   - Check network connectivity to weather API

3. **Web Interface Not Loading**
   - Confirm Flask app is running on correct port
   - Check for port conflicts

### Debug Mode
Enable debug logging by setting `debug=True` in `config.py`:

```python
FLASK_CONFIG = {
    'debug': True
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain**: For the agent framework
- **Ollama**: For local LLM serving
- **MCP Protocol**: For weather service integration
- **Flask**: For the web framework

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the logs for error details
3. Open an issue on GitHub with:
   - Error description
   - Steps to reproduce
   - System information
   - Relevant log output

---

**Built with ❤️ using LangChain, Flask, and Ollama** 