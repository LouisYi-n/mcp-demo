# zdlang-agent 智能代理项目

## 🚀 项目概述

zdlang-agent 是一个基于 AI 的智能代理系统，使用智能路由技术自动识别用户意图并调用相应的工具处理器。项目采用模块化架构设计，支持多种工具集成，具备强大的扩展性。

## ✨ 核心特性

- **🧠 智能路由**: 双重路由机制（规则路由 + AI路由）自动识别用户意图
- **🛠️ 工具集成**: 支持天气查询、新闻获取、翻译、计算器、通用对话等多种工具
- **🔧 模块化架构**: 清晰的代码组织结构，易于维护和扩展
- **🌐 Web界面**: 友好的聊天界面，实时交互体验
- **🔄 热重载**: 开发模式下支持代码热重载
- **📊 智能错误处理**: 友好的错误提示和异常处理

## 🏗️ 项目结构

```
zdlang-agent/
├── app.py              # 🎯 主应用入口文件
├── config.py           # ⚙️ 配置文件
├── web_agent.py        # 📄 原始单文件版本（已重构）
├── zdlang-agent.md     # 📖 项目说明文档
├── requirements.txt    # 📦 依赖包列表
├── core/               # 🔧 核心组件
│   ├── __init__.py
│   ├── base.py         # 工具处理器基类
│   └── router.py       # 智能路由器
├── handlers/           # 🛠️ 工具处理器模块  
│   ├── __init__.py
│   ├── weather.py      # 天气查询处理器
│   ├── chat.py         # 通用对话处理器
│   ├── news.py         # 新闻查询处理器
│   ├── translation.py  # 翻译处理器
│   └── calculator.py   # 计算器处理器
├── services/           # 🌐 外部服务接口
│   ├── __init__.py
│   ├── ollama.py       # Ollama API 服务
│   └── weather_api.py  # 天气 API 服务
├── utils/              # 🔨 工具函数
│   ├── __init__.py
│   └── text_utils.py   # 文本处理工具
└── templates/          # 🎨 前端模板
    └── index.html      # Web界面模板
```

## 🚀 快速启动

### 前置依赖

确保以下服务正在运行：
- **Ollama**: `http://localhost:11434` (使用 deepseek-r1:7b 模型)
- **天气API服务**: `http://localhost:8081`

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动应用

```bash
# 进入项目目录
cd lang-agent/zdlang-agent

# 启动应用
python app.py
```

### 访问应用

启动成功后，访问: **http://localhost:5001**

## 🏛️ 技术架构

### 1. 智能路由系统

zdlang-agent 采用双重路由机制：

#### 规则路由 (Rule-based Routing)
- 基于关键词匹配
- 快速响应常见问题
- 高精度识别特定领域

#### AI路由 (AI-based Routing)
- 使用 Ollama 模型进行意图识别
- 处理复杂和模糊的用户输入
- 智能选择最合适的工具处理器

### 2. 工具处理器架构

```python
# 基础处理器接口
class ToolHandler(ABC):
    @abstractmethod
    def get_tool_name(self) -> str: pass
    
    @abstractmethod
    def get_description(self) -> str: pass
    
    @abstractmethod
    def can_handle(self, query: str) -> bool: pass
    
    @abstractmethod
    def handle(self, query: str) -> dict: pass
```

### 3. 服务层架构

- **Ollama服务**: 提供AI模型推理能力
- **天气API服务**: 提供天气数据查询
- **文本处理服务**: 提供文本清理和格式化

## 🛠️ 可用工具

| 工具 | 描述 | 触发关键词 | 状态 |
|------|------|------------|------|
| 🌤️ 天气查询 | 查询城市天气信息 | 天气、气温、下雨等 | ✅ 已实现 |
| 📰 新闻查询 | 获取最新新闻资讯 | 新闻、资讯、热点等 | 🚧 开发中 |
| 🌐 翻译服务 | 多语言文本翻译 | 翻译、英文、中文等 | 🚧 开发中 |
| 🧮 计算器 | 数学计算功能 | 计算、算、数学等 | 🚧 开发中 |
| 🤖 通用对话 | AI对话交互 | 默认处理器 | ✅ 已实现 |

## 🔧 配置说明

### config.py 配置参数

```python
# 服务配置
FLASK_HOST = '0.0.0.0'          # Flask服务主机
FLASK_PORT = 5001               # Flask服务端口
FLASK_DEBUG = True              # 调试模式

# 外部服务配置
OLLAMA_BASE_URL = 'http://localhost:11434'      # Ollama API地址
OLLAMA_MODEL = 'deepseek-r1:7b'                 # 使用的AI模型
WEATHER_API_BASE_URL = 'http://localhost:8081'  # 天气API地址
```

## 📈 扩展开发

### 添加新的工具处理器

1. 在 `handlers/` 目录下创建新的处理器文件
2. 继承 `ToolHandler` 基类
3. 实现必要的方法
4. 在 `app.py` 中注册处理器

示例：

```python
# handlers/new_tool.py
from core.base import ToolHandler

class NewToolHandler(ToolHandler):
    def get_tool_name(self) -> str:
        return "new_tool"
    
    def get_description(self) -> str:
        return "新工具描述"
    
    def can_handle(self, query: str) -> bool:
        return "关键词" in query
    
    def handle(self, query: str) -> dict:
        # 处理逻辑
        return {"think": "思考过程", "answer": "最终答案"}
```

### 添加新的服务接口

1. 在 `services/` 目录下创建服务文件
2. 实现具体的API调用逻辑
3. 在对应的处理器中调用服务

## 🐛 故障排除

### 常见问题

1. **端口冲突**: 修改 `config.py` 中的 `FLASK_PORT`
2. **Ollama连接失败**: 确保 Ollama 服务运行在 11434 端口
3. **天气API无响应**: 检查天气服务是否在 8081 端口运行
4. **模块导入错误**: 确保在项目根目录下启动应用

### 日志调试

应用启动时会显示详细的日志信息：
- 工具处理器注册情况
- 服务依赖检查
- 错误和异常信息

## 📝 开发记录

### 架构演进

1. **v1.0**: 单文件架构，基于 if-else 逻辑
2. **v2.0**: 引入智能路由和工具处理器模式
3. **v3.0**: 模块化重构，清晰的代码组织结构

### 主要改进

- ✅ 智能路由替代硬编码逻辑
- ✅ 模块化架构提升可维护性
- ✅ 错误处理和用户体验优化
- ✅ Web界面交互体验提升

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交变更
4. 发起 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

---

🎉 **欢迎使用 zdlang-agent！** 如有问题，请查看文档或提交 Issue。 
