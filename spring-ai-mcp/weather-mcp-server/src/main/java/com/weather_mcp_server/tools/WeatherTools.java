package com.weather_mcp_server.tools;

import java.util.HashMap;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

/**
 * @author louis
 * @version 1.0
 * @date 2025/5/21 16:03
 */
@Service
public class WeatherTools {

    @Value("${amap.api.key}")
    private String apiKey;

    @Value("${amap.api.weather.url}")
    private String weatherUrl;


    private final RestTemplate restTemplate = new RestTemplate();

    @Tool(name="getWeather", description = "Get weather information by city name")
    public String getWeather(@ToolParam(description = "city name")String cityName) {
        if (cityName == null || cityName.isEmpty()) {
            return "City name cannot be empty";
        }

        String adCode = switch (cityName) {
            case "武汉" -> "420100";
            case "广州" -> "440100";
            case "深圳" -> "440300";
            case "北京" -> "110100";
            default -> null;
        };

        if (adCode == null) {
            return "抱歉，当前仅支持查询以下城市的天气：武汉、广州、深圳、北京";
        }

        String url = weatherUrl + "?city={city}&key={key}&extensions=base&output=JSON";
        var uriVariables = new HashMap<String, Object>();
        uriVariables.put("city", adCode);
        uriVariables.put("key", apiKey);
        try {
            String response = restTemplate.getForObject(url, String.class, uriVariables);
            return response;
        } catch (Exception e) {
            return "当前服务不可用: " + e.getMessage();
        }
    }

}
