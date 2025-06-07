package com.spring_ai_ollama;

import com.spring_ai_ollama.tools.WeatherTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiOllamaApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringAiOllamaApplication.class, args);
	}

}
