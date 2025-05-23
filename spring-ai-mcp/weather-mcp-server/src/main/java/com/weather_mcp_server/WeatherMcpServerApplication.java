package com.weather_mcp_server;

import com.weather_mcp_server.tools.WeatherTools;
import io.modelcontextprotocol.server.McpServerFeatures.SyncPromptSpecification;
import io.modelcontextprotocol.spec.McpSchema;
import java.util.List;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import io.modelcontextprotocol.server.McpServerFeatures;


@SpringBootApplication
public class WeatherMcpServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(WeatherMcpServerApplication.class, args);
	}
	@Bean
	public ToolCallbackProvider toolCallbacks(WeatherTools weatherTools) {
		return MethodToolCallbackProvider.builder()
			.toolObjects(weatherTools)
			.build();
	}

	@Bean
	public List<McpServerFeatures.SyncPromptSpecification> prompts() {
		var prompt = new McpSchema.Prompt("weather-by-city-name", "Get weather information by city name",
			List.of(new McpSchema.PromptArgument("city-name", "city name", true)));

		var promptRegistration = new McpServerFeatures.SyncPromptSpecification(prompt, (exchange, getPromptRequest) -> {
			String argument = (String) getPromptRequest.arguments().get("city-name");
			var userMessage = new McpSchema.PromptMessage(McpSchema.Role.USER,
				new McpSchema.TextContent("What's the weather " + argument + " of today?"));
			return new McpSchema.GetPromptResult("Get weather of today by city name", List.of(userMessage));
		});

		return List.of(promptRegistration);
	}
}
