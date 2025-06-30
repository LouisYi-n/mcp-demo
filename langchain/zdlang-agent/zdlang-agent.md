# zdlang-agent (LangChain-based Intelligent Agent)

## Project Overview
zdlang-agent is an intelligent agent project based on the LangChain framework that can automatically choose to call local large language models (deepseek-r1:7b/Ollama) or local MCP weather services based on user questions. The project adopts a simplified intelligent routing mechanism to avoid complex ReAct format issues.

**Core Features:**
- 🌤️ **Weather Queries**: Automatically identifies weather-related questions and calls MCP weather service
- 💬 **Intelligent Conversations**: Handles general questions, knowledge Q&A, joke telling, etc., calling local Ollama large models
- 🎯 **Smart Routing**: Intent recognition based on keyword matching, no complex ReAct format required
- 🌐 **Web Interface**: Provides friendly web chat interface with real-time interaction support

## Technical Architecture

### Project Structure
```
zdlang-agent/
├── app.py                  # Flask Web API entry point, HTTP service
├── agent.py                # Simplified intelligent agent implementation (SimpleAgent)
├── config.py               # Unified configuration management
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web chat interface
├── tools/                 # LangChain toolset
│   ├── weather_tool.py    # MCP weather query tool
│   └── chat_tool.py       # Ollama conversation tool
├── core/                  # Core foundation modules
│   ├── __init__.py
│   └── base.py
├── services/              # External service wrappers
│   ├── weather_api.py     # Weather API service
│   ├── ollama.py          # Ollama service
│   └── __init__.py
└── utils/                 # Utility functions
```

### Core Components

#### 1. SimpleAgent (agent.py)
```python
class SimpleAgent:
    """Simplified intelligent agent to avoid complex ReAct format issues"""
    
    def invoke(self, inputs):
        query = inputs.get("input", "")
        
        # Intelligent routing: determine intent based on keywords
        if self._is_weather_query(query):
            return self._handle_weather(query)
        else:
            return self._handle_chat(query)
```

**Features:**
- Intelligent routing based on keyword matching
- Avoids LLM output format error issues
- Supports two modes: weather queries and general conversations
- Returns standardized result format

#### 2. Tool System (tools/)

**Weather Tool (weather_tool.py):**
- Calls local MCP weather service (localhost:8081)
- Parses fixed-format JSON weather data
- Formats output into natural language
- Supports error handling and timeout processing

**Chat Tool (chat_tool.py):**
- Integrates Ollama local large model (deepseek-r1:7b)
- Cleans `<think>` tags from LLM output
- Supports general conversations, knowledge Q&A, joke telling, etc.

#### 3. Web Service (app.py)
- Flask HTTP API service
- RESTful interface design
- Real-time chat interface
- Tool calling process display

## Main Dependencies

### Python Packages
```txt
langchain              # LangChain core framework
langchain-community    # Community extensions
langchain-core         # Core components
flask                  # Web framework
requests              # HTTP client
```

### External Services
- **Ollama**: Local large model service (localhost:11434)
  - Model: deepseek-r1:7b
  - Purpose: General conversations, knowledge Q&A
- **MCP Weather Service**: Local weather API (localhost:8081)
  - Provides city weather queries
  - Returns standard JSON format data

## API Interfaces

### 1. Main Query Interface
```bash
POST /api/query
Content-Type: application/json

{
  "query": "How's the weather in Beijing?"
}
```

**Response Format:**
```json
{
  "result": "Beijing current weather: sunny, temperature 25°C, south wind ≤3 level, humidity 65%",
  "tool_calls": ["🔧 I called weather MCP, result: ..."]
}
```

### 2. Tools List Interface
```bash
GET /api/tools
```

### 3. Health Check Interface
```bash
GET /health
```

## Intelligent Routing Mechanism

### Weather Query Recognition
**Keyword List:**
```python
weather_keywords = [
    "weather", "temperature", "temp", "rain", "sunny", "cloudy", "wind", 
    "overcast", "rainy", "snowy", "typhoon", "humidity", "forecast",
    # Chinese keywords for compatibility
    "天气", "气温", "温度", "下雨", "晴天", "阴天", "刮风", 
    "多云", "雨天", "雪天", "台风", "湿度", "风力"
]
```

**Supported Cities:**
- Major cities: Beijing, Shanghai, Guangzhou, Shenzhen, Wuhan, Chengdu, etc.
- Default city: Beijing (when no specific city is identified)

### Processing Flow
1. **Intent Recognition**: Check if query contains weather keywords
2. **Route Dispatch**: 
   - Weather queries → weather_tool → MCP service
   - Other questions → chat_tool → Ollama model
3. **Result Processing**: Format output and return tool calling information

## Usage Guide

### 1. Environment Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Ollama service (needs to be pre-installed)
ollama serve

# Pull model
ollama pull deepseek-r1:7b

# Start MCP weather service (needs separate deployment)
# Ensure localhost:8081 is accessible
```

### 2. Start Application
```bash
python app.py
```

**Service Information:**
- Web interface: http://localhost:5001
- API endpoints: http://localhost:5001/api/*
- Debug mode: Enabled by default

### 3. Usage Examples

**Weather Query:**
```
User: "How's the weather in Shenzhen?"
System: 🔧 I called weather MCP, result: Shenzhen current weather: overcast, temperature 27°C, southeast wind ≤3 level, humidity 80%
```

**General Conversation:**
```
User: "Tell me a joke"
System: One day, a cat met a dog...
```

## Configuration

### config.py Main Configuration
```python
# Service Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
FLASK_DEBUG = True

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "deepseek-r1:7b"

# Weather API Configuration
WEATHER_API_BASE_URL = "http://localhost:8081"
WEATHER_API_TIMEOUT = 10
```

## Extension Development

### 1. Adding New Tools
```python
# 1. Create tool function
def new_tool_func(input_param: str) -> str:
    # Implement specific functionality
    return result

# 2. Create LangChain tool
new_tool = Tool(
    name="new_tool",
    func=new_tool_func,
    description="Tool description"
)

# 3. Register to agent
tools = [weather_tool, chat_tool, new_tool]
```

### 2. Extend Routing Logic
Add new intent recognition logic in `SimpleAgent._is_weather_query()`.

### 3. Change Large Model
Modify `OLLAMA_MODEL` configuration in `config.py`, supports any Ollama-compatible model.

## Project Features

### ✅ Advantages
- **Simple Architecture**: Avoids complex ReAct format, uses keyword routing
- **Stable Response**: Doesn't rely on LLM output format, reduces parsing errors
- **Easy to Extend**: Standard LangChain tool interface
- **User Friendly**: Intuitive web interface, real-time interaction experience
- **Local Deployment**: Completely localized, secure and controllable data

### 🎯 Use Cases
- Personal intelligent assistant
- Enterprise internal knowledge Q&A
- Local AI service deployment
- LangChain learning and experimentation

## References
- [LangChain Official Documentation](https://python.langchain.com/)
- [Ollama Official Documentation](https://ollama.com/)
- [Flask Official Documentation](https://flask.palletsprojects.com/)

---

**Project Status**: ✅ Production Ready  
**Version**: v1.0.0  
**Last Updated**: 2025-06-30
