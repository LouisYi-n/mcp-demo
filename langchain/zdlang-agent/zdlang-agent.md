# zdlang-agent (基于 LangChain 的智能代理)

## 项目简介
zdlang-agent 是一个基于 LangChain 框架的智能代理（Agent）项目，能够根据用户问题自动选择调用本地大模型（deepseek-r1:7b/Ollama）或本地 MCP 天气服务。项目采用简化的智能路由机制，避免了复杂的 ReAct 格式问题。

**核心功能：**
- 🌤️ **天气查询**：自动识别天气相关问题，调用 MCP 天气服务
- 💬 **智能对话**：处理一般问题、知识问答、讲笑话等，调用本地 Ollama 大模型
- 🎯 **智能路由**：基于关键词匹配的意图识别，无需复杂的 ReAct 格式
- 🌐 **Web界面**：提供友好的 Web 聊天界面，支持实时交互

## 技术架构

### 项目结构
```
zdlang-agent/
├── app.py                  # Flask Web API 入口，HTTP服务
├── agent.py                # 简化智能代理实现 (SimpleAgent)
├── config.py               # 统一配置管理
├── requirements.txt        # Python依赖包
├── templates/
│   └── index.html         # Web聊天界面
├── tools/                 # LangChain工具集
│   ├── weather_tool.py    # MCP天气查询工具
│   └── chat_tool.py       # Ollama对话工具
├── core/                  # 核心基础模块
│   ├── __init__.py
│   └── base.py
├── services/              # 外部服务封装
│   ├── weather_api.py     # 天气API服务
│   ├── ollama.py          # Ollama服务
│   └── __init__.py
└── utils/                 # 工具函数
```

### 核心组件

#### 1. SimpleAgent (agent.py)
```python
class SimpleAgent:
    """简化的智能代理，避免复杂的ReAct格式问题"""
    
    def invoke(self, inputs):
        query = inputs.get("input", "")
        
        # 智能路由：根据关键词判断意图
        if self._is_weather_query(query):
            return self._handle_weather(query)
        else:
            return self._handle_chat(query)
```

**特点：**
- 基于关键词匹配的智能路由
- 避免 LLM 输出格式错误问题
- 支持天气查询和一般对话两种模式
- 返回标准化的结果格式

#### 2. 工具系统 (tools/)

**天气工具 (weather_tool.py):**
- 调用本地 MCP 天气服务 (localhost:8081)
- 解析固定格式的 JSON 天气数据
- 格式化成自然语言输出
- 支持错误处理和超时处理

**对话工具 (chat_tool.py):**
- 集成 Ollama 本地大模型 (deepseek-r1:7b)
- 清理 LLM 输出中的 `<think>` 标签
- 支持通用对话、知识问答、讲笑话等

#### 3. Web服务 (app.py)
- Flask HTTP API 服务
- RESTful 接口设计
- 实时聊天界面
- 工具调用过程展示

## 主要依赖

### Python包
```txt
langchain              # LangChain核心框架
langchain-community    # 社区扩展包
langchain-core         # 核心组件
flask                  # Web框架
requests              # HTTP客户端
```

### 外部服务
- **Ollama**: 本地大模型服务 (localhost:11434)
  - 模型: deepseek-r1:7b
  - 用途: 通用对话、知识问答
- **MCP天气服务**: 本地天气API (localhost:8081)
  - 提供城市天气查询
  - 返回标准JSON格式数据

## API接口

### 1. 主要查询接口
```bash
POST /api/query
Content-Type: application/json

{
  "query": "北京天气怎么样？"
}
```

**响应格式:**
```json
{
  "result": "北京当前天气：晴，温度25°C，南风≤3级，湿度65%",
  "tool_calls": ["🔧 我调用了 weather MCP，结果是：..."]
}
```

### 2. 工具列表接口
```bash
GET /api/tools
```

### 3. 健康检查接口
```bash
GET /health
```

## 智能路由机制

### 天气查询识别
**关键词列表:**
```python
weather_keywords = [
    "天气", "气温", "温度", "下雨", "晴天", "阴天", "刮风", 
    "多云", "雨天", "雪天", "台风", "湿度", "风力"
]
```

**支持城市:**
- 主要城市: 北京、上海、广州、深圳、武汉、成都等
- 默认城市: 北京（当未识别到具体城市时）

### 处理流程
1. **意图识别**: 检查查询中是否包含天气关键词
2. **路由分发**: 
   - 天气查询 → weather_tool → MCP服务
   - 其他问题 → chat_tool → Ollama模型
3. **结果处理**: 格式化输出并返回工具调用信息

## 使用指南

### 1. 环境准备
```bash
# 安装Python依赖
pip install -r requirements.txt

# 启动Ollama服务 (需要预先安装)
ollama serve

# 拉取模型
ollama pull deepseek-r1:7b

# 启动MCP天气服务 (需要单独部署)
# 确保 localhost:8081 可访问
```

### 2. 启动应用
```bash
python app.py
```

**服务信息:**
- Web界面: http://localhost:5001
- API端点: http://localhost:5001/api/*
- 调试模式: 默认开启

### 3. 使用示例

**天气查询:**
```
用户: "深圳天气怎么样？"
系统: 🔧 我调用了 weather MCP，结果是：深圳市当前天气：阴，温度27°C，东南风≤3级，湿度80%
```

**一般对话:**
```
用户: "讲个笑话"
系统: 有一天，一只猫遇到了一只狗...
```

## 配置说明

### config.py 主要配置
```python
# 服务配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5001
FLASK_DEBUG = True

# Ollama配置
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "deepseek-r1:7b"

# 天气API配置
WEATHER_API_BASE_URL = "http://localhost:8081"
WEATHER_API_TIMEOUT = 10
```

## 扩展开发

### 1. 添加新工具
```python
# 1. 创建工具函数
def new_tool_func(input_param: str) -> str:
    # 实现具体功能
    return result

# 2. 创建LangChain工具
new_tool = Tool(
    name="new_tool",
    func=new_tool_func,
    description="工具描述"
)

# 3. 注册到agent
tools = [weather_tool, chat_tool, new_tool]
```

### 2. 扩展路由逻辑
在 `SimpleAgent._is_weather_query()` 中添加新的意图识别逻辑。

### 3. 更换大模型
修改 `config.py` 中的 `OLLAMA_MODEL` 配置，支持任何Ollama兼容的模型。

## 项目特点

### ✅ 优势
- **架构简洁**: 避免复杂的ReAct格式，使用关键词路由
- **响应稳定**: 不依赖LLM输出格式，减少解析错误
- **易于扩展**: 标准的LangChain工具接口
- **用户友好**: 直观的Web界面，实时交互体验
- **本地部署**: 完全本地化，数据安全可控

### 🎯 适用场景
- 个人智能助手
- 企业内部知识问答
- 本地化AI服务部署
- LangChain学习和实验

## 参考资源
- [LangChain 官方文档](https://python.langchain.com/)
- [Ollama 官方文档](https://ollama.com/)
- [Flask 官方文档](https://flask.palletsprojects.com/)

---

**项目状态**: ✅ 生产就绪  
**版本**: v1.0.0  
**最后更新**: 2025-06-30
