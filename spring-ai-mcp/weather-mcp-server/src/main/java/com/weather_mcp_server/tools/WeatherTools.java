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
            case "广州市" -> "440100";
            case "深圳" -> "440300";
            default -> null;
        };

        String url = weatherUrl + "?city={city}&key={key}&extensions=base&output=JSON";
        var uriVariables = new HashMap<String, Object>();
        uriVariables.put("city", adCode);
        uriVariables.put("key", apiKey);
        try {
            String response = restTemplate.getForObject(url, String.class, uriVariables);
            return response;
        } catch (Exception e) {
            return "Failed to fetch weather data: " + e.getMessage();
        }
    }

}
