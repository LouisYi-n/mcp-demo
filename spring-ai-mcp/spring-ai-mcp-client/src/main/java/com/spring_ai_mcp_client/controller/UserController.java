package com.spring_ai_mcp_client.controller;

import static com.spring_ai_mcp_client.prompt.UserPromptTemplates.CREATE_USER;

import com.spring_ai_mcp_client.prompt.UserPromptTemplates;
import io.modelcontextprotocol.client.McpAsyncClient;
import java.util.List;
import java.util.Map;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
/**
 * @author louis
 * @version 1.0
 * @date 2025/5/27 22:03
 */
@RestController
@RequestMapping("/user")
public class UserController {

    private final ChatClient chatClient;
    private final List<McpAsyncClient> mcpSyncClients;

    public UserController(ChatClient.Builder chatClientBuilder,
        ToolCallbackProvider tools,
        List<McpAsyncClient> mcpSyncClients) {
        this.chatClient = chatClientBuilder
            .defaultToolCallbacks(tools)
            .build();
        this.mcpSyncClients = mcpSyncClients;
    }

    @PostMapping("/create")
    public Object createUser(@RequestBody Map<String, Object> userInfo) {
        Prompt p = UserPromptTemplates.CREATE_USER.create(userInfo);
          return this.chatClient.prompt(p);
    }

    @GetMapping("/by-login")
    public Object getUserByLogin(@RequestParam String login) {
        PromptTemplate pt = UserPromptTemplates.GET_USER_BY_LOGIN;
        return this.chatClient.prompt(pt.create(Map.of("login", login)));
    }

    @GetMapping("/by-email")
    public Object getUsersByEmail(@RequestParam String email) {
        PromptTemplate pt = UserPromptTemplates.GET_USERS_BY_EMAIL;
        return this.chatClient.prompt(pt.create(Map.of("email", email)));
    }
}
