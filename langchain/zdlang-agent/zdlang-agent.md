# zdlang-agent (基于 LangChain)

## 项目简介
zdlang-agent 是一个基于 LangChain 框架的智能代理（Agent）项目，能够根据用户问题自动选择调用本地大模型（如 deepseek-r1-7b/Ollama）或本地 MCP 天气服务。

- 当你询问城市天气时，Agent 会自动访问 MCP 天气服务。
- 当你提其他问题时，Agent 会自动调用本地 Ollama 的大模型进行回答。

## 技术架构与核心模块

```
zdlang-agent/
├── app.py              # Flask Web API 入口，接收用户请求
├── agent.py            # LangChain Agent 组装与初始化
├── tools/
│   ├── weather_tool.py # MCP 天气查询 Tool
│   └── chat_tool.py    # 通用对话 Tool（Ollama LLM）
├── requirements.txt    # 依赖包列表（含 langchain、flask、requests 等）
└── ...
```

## 主要依赖
- langchain
- langchain-community
- flask
- requests
- 本地 Ollama 服务（如 deepseek-r1:7b）
- MCP 天气服务

## LangChain 主要用到的模块
- `langchain.agents`：Agent 组装与推理
- `langchain.tools`：自定义工具（Tool）封装
- `langchain_community.llms`：本地 LLM（Ollama）集成

## 智能路由与工具机制
- 所有功能均通过 LangChain Agent 统一调度。
- AgentType 采用 ZERO_SHOT_REACT_DESCRIPTION，LLM 根据用户输入和 Tool 描述自动选择合适工具。
- 天气查询、通用对话等均以 Tool 形式注册到 Agent。
- 无需手写 if/else 规则，完全依赖 LLM 语义理解和工具描述。

## 典型用法

### 1. 启动服务
```bash
pip install -r requirements.txt
python app.py
```

### 2. 发送请求
```bash
curl -X POST http://localhost:5001/chat -H "Content-Type: application/json" -d '{"query": "北京天气怎么样？"}'
```

### 3. Agent 智能决策
- 用户问天气 → 自动调用 weather_tool → MCP 天气API
- 用户问其他 → 自动调用 chat_tool → Ollama LLM

## 扩展建议
- 新增 Tool 只需实现 func 并注册到 Agent。
- 可扩展多轮对话（加 memory）、RAG 检索、更多外部 API 工具。
- 支持切换 LLM（如 OpenAI、Qwen、ChatGLM 等）。

## 参考
- [LangChain 官方文档](https://python.langchain.com/)
- [Ollama 官方文档](https://ollama.com/)
- [LangChain Tool 机制](https://python.langchain.com/docs/modules/agents/tools/)

---

如需进一步定制开发、Agent 设计、RAG 方案等，欢迎随时交流！
