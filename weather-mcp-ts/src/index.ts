import {McpServer} from "@modelcontextprotocol/sdk/server/mcp.js";
import {StdioServerTransport} from "@modelcontextprotocol/sdk/server/stdio.js";
import {z} from "zod";
import axios from 'axios';
import {getCityAdcode} from './cityCodeApi.js';

console.error('当前工作目录 main:', process.cwd());

const WEATHER_API_URL = "https://restapi.amap.com/v3/weather/weatherInfo";
const API_KEY = "a96fb21077e099320816b426df45c1bd";

// 实例化一个MCP服务器
const mcpServer = new McpServer({
  name: "weather",
  version: "1.0.0",
}, {
  capabilities: {
    logging: {} // 开启日志记录，必须，不然报错
  }
});

interface WeatherResponse {
  status: string;
  count: string;
  info: string;
  infocode: string;
  lives: Weather[];
}

interface Weather {
  province: string;
  city: string;
  adcode: string;
  weather: string;
  temperature: string;
  winddirection: string;
  windpower: string;
  humidity: string;
  reporttime: string;
}

/**
 * 获取天气信息
 * @param cityAdcode 城市 adCode
 */
async function getWeather(cityAdcode: string): Promise<WeatherResponse> {
  try {
    const response = await axios.get<WeatherResponse>(
        `${WEATHER_API_URL}?key=${API_KEY}&city=${cityAdcode}&extensions=base&output=JSON`
    );

    if (response.data.status === '1') {
      //const WeatherResponse = response.data.lives[0];
      console.info(`API 正确返回了数据`);
    } else {
      console.error(`错误信息: ${response.data.info}`);
    }
    return response.data;
  } catch (error) {
    console.error('请求失败:', error);
    throw new Error("天气信息获取失败");
  }
}


// 定义MCP工具
// 名称为 getWeather
// 描述为 获取某个城市的天气信息---> 描述十分的重要，大模型会根据描述选择 MCP 进行生成
// 参数为 city，这里MCP使用了 zod 来定义参数类型
// 第四个参数为回调函数，用于处理具体的逻辑
// 定义MCP工具
mcpServer.tool(
    "getWeather",
    "获取某个城市的天气信息",
    {
      city: z.string().describe("城市名称"),
    },
    async ({city}) => {
      // 假设您有一个方法可以将城市名称转换为城市编码
      const cityAdcode = await getCityAdcode(city); // 需要自行实现这个转换

      // 调用 `getWeather` 方法并处理返回值
      const res = await getWeather(cityAdcode);

      // 由于 getWeather 函数返回的结构是 WeatherResponse,
      // 因此需要根据响应进行错误处理
      if (res.status !== '1') {
        return {
          content: [
            {
              type: "text",
              text: "获取天气信息失败: " + res.info,
            },
          ],
        };
      }

      // 从返回的天气信息中获取实时天气数据
      const weather = res.lives[0];
      let txt = `${city} 的天气信息：\n`;
      txt += `实时天气：${weather.weather}，温度：${weather.temperature}°C，风向：${weather.winddirection}，风力：${weather.windpower}，湿度：${weather.humidity}%\n`;
      txt += `报告时间：${weather.reporttime}`;

      // 返回结果，content是个数组
      return {
        content: [
          {
            type: "text",
            text: txt,
          },
        ],
      };
    }
);

async function main() {
  // 本地服务，这里使用 stdio 传输
  const transport = new StdioServerTransport();
  await mcpServer.connect(transport);
  console.log('当前工作目录 main:', process.cwd());
  console.error("Weather MCP Server running on stdio");
  mcpServer.server.sendLoggingMessage({
    level: 'info',
    data: 'Server started successfully',
  });
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
