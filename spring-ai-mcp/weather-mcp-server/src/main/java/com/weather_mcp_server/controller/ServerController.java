package com.weather_mcp_server.controller;

import com.weather_mcp_server.tools.WeatherTools;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author louis
 * @version 1.0
 * @date 2025/5/21 15:55
 */


@RestController
public class ServerController {
    @Value("${server.port}")
    private String port;

    @Autowired
    private WeatherTools weatherTools;

    @GetMapping("/api/info")
    public String getServerInfo() {
        return "Response from MCP Server (Port: " + port + ")";
    }

    @GetMapping("/api/weather")
    public String test(@RequestParam String cityName) {
        return weatherTools.getWeather(cityName);
    }
}
