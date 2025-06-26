# zdlang-agent

## 项目简介
zdlang-agent 是一个基于 LangChain 的智能代理（Agent）项目，能够根据用户问题自动选择调用本地大模型（如 deepseek-r1-7b）或本地 mcp-server 查询天气。

- 当你询问城市天气时，Agent 会自动访问 mcp-server 查询天气。
- 当你提其他问题时，Agent 会自动调用本地 Ollama 的 deepseek-r1-7b 进行回答。

## 主要特性
- 智能路由：根据问题内容自动选择调用天气服务或大模型。
- 支持本地大模型推理。
- 可扩展，便于集成更多工具。

## 使用方法

### 1. 环境准备
- Windows 11 系统
- Python 3.9+
- 已安装 [Ollama](https://ollama.com/) 并运行 deepseek-r1-7b
- 已运行 mcp-server（本地天气查询服务）
- 已运行 Open-WebUI（可选，便于交互）

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动 Agent
```bash
python agent.py
```

### 4. 交互方式
- 通过命令行输入问题，Agent 会自动判断调用天气服务或大模型。

## 目录结构
- agent.py         # 主程序，Agent 实现
- requirements.txt # 依赖包列表
- README.md        # 项目说明
- Create-agent.md  # 构建步骤说明

## 联系方式
如有问题请联系项目维护者。 