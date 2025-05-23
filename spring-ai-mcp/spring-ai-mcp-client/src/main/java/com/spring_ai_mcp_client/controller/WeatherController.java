package com.spring_ai_mcp_client.controller;

import io.modelcontextprotocol.client.McpAsyncClient;
import io.modelcontextprotocol.spec.McpSchema;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author louis
 * @version 1.0
 * @date 2025/5/22 14:40
 */
@Slf4j
@RestController
@RequestMapping("/weather")
public class WeatherController {


    private final ChatClient chatClient;
    private final List<McpAsyncClient> mcpSyncClients;

    public WeatherController(ChatClient.Builder chatClientBuilder,
        ToolCallbackProvider tools,
        List<McpAsyncClient> mcpSyncClients) {
        log.info("WeatherController initialized with parameters:");
        log.info("ToolCallbackProvider: {}", tools);
        log.info("Number of McpAsyncClients: {}", (mcpSyncClients != null ? mcpSyncClients.size() : 0));
        this.chatClient = chatClientBuilder
            .defaultToolCallbacks(tools)
            .build();
        this.mcpSyncClients = mcpSyncClients;
    }

    @GetMapping()
    String getWeather(@RequestParam("cityName") String cityName) {
        PromptTemplate pt = new PromptTemplate("""
                What's the weather like in {cityName} today? ?
                """);
        Prompt p = pt.create(Map.of("cityName", cityName));
        return this.chatClient.prompt(p)
            .call()
            .content();
    }

    Prompt loadPromptByName(String name, String cityName) {
        McpSchema.GetPromptRequest r = new McpSchema.GetPromptRequest(name, Map.of("cityName", cityName));
        var client = mcpSyncClients.stream()
            .filter(c -> c.getServerInfo().name().equals("weather-mcp-server"))
            .findFirst();
        if (client.isPresent()) {
            var content = (McpSchema.TextContent) client.get().getPrompt(r).block().messages().get(0).content();
            PromptTemplate pt = new PromptTemplate(content.text());
            Prompt p = pt.create(Map.of("cityName", cityName));
            log.info("Prompt: {}", p);
            return p;
        } else return null;
    }
}
