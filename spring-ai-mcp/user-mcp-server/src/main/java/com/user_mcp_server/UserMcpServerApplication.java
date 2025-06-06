package com.user_mcp_server;

import com.user_mcp_server.tools.UserTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class UserMcpServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(UserMcpServerApplication.class, args);
	}
	@Bean
	public ToolCallbackProvider toolCallbacks(UserTools userTools) {
		return MethodToolCallbackProvider.builder()
			.toolObjects(userTools)
			.build();
	}
}
