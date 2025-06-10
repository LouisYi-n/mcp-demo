# Weather MCP Server

这是一个基于 Spring Boot 的天气 MCP Server，它提供了天气查询功能，支持查询北京、武汉、广州和深圳的天气信息。

## 功能特点

- 基于 Spring Boot 3.4.5 构建
- 集成高德地图天气 API
- 支持查询多个城市的实时天气
- 提供 RESTful API 接口
- 支持 MCP (Model Context Protocol) 集成

## 快速开始

### 1. 环境要求

- JDK 17 或更高版本
- Maven 3.9.9 或更高版本
- 高德地图 API Key（已配置）

### 2. 运行服务

```bash
./mvnw spring-boot:run
```

服务将在 8081 端口启动。

### 3. API 接口

#### 服务器信息

```bash
GET http://localhost:8081/api/info
```

#### 天气查询

```bash
GET http://localhost:8081/api/weather?cityName={城市名}
```

支持的城市：北京、武汉、广州、深圳

## Cursor MCP 配置

### 1. Prompt
```
我希望你能够：
1. 直接调用已配置好的 MCP Server
2. 清晰地说明调用了哪个 MCP Server 以及做了什么操作
3. 展示调用结果
4. 如果遇到错误，能够根据错误信息进行适当的处理和回答
```


### 2. 配置步骤

1. 在 Cursor 中打开设置
2. 找到 MCP 配置部分
3. 添加新的 MCP Server 配置：
   ```json
   {
     "mcpServers": {
       "weather-mcp-server": {
         "url": "http://localhost:8081",
         "description": "本地 Spring AI MCP Server，提供天气查询功能",
         "icon": "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png",
         "type": "mcp"
       }
     }
   }
   ```
### 3. 使用示例

当配置完成后，您可以在 Cursor 中直接使用以下格式调用天气服务：

```

我调用了本地的 Weather MCP Server 去查询北京的天气，结果如下：

- 天气状况：晴
- 温度：32℃
- 风向：西南
- 风力：≤3级
- 湿度：16%

```

## 错误处理

当遇到错误时，服务会返回适当的错误信息：

1. 城市不支持：
   ```
   抱歉，当前仅支持查询以下城市的天气：武汉、广州、深圳、北京
   ```


2. API 调用失败：
   ```
   当前服务不可用: {具体错误信息}
   ```

## 参考文档

- [Spring Boot 文档](https://docs.spring.io/spring-boot/3.4.5/reference)
- [Spring AI MCP Server 文档](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html)
- [高德地图天气 API 文档](https://lbs.amap.com/api/webservice/guide/api/weatherinfo)

## 注意事项

- 请确保在使用前已正确配置高德地图 API Key
- 服务默认运行在 8081 端口，如需修改请更新 application.properties
- 当前仅支持查询指定城市的天气信息
