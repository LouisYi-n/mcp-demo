package com.user_mcp_server.controller;

import com.user_mcp_server.model.User;
import com.user_mcp_server.tools.UserTools;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author louis
 * @version 1.0
 * @date 2025/5/27 21:08
 */
@RestController
@RequestMapping("/api")
public class UserController {

    @Value("${server.port}")
    private String port;

    @Autowired
    private UserTools userTools;

    @GetMapping("/info")
    public String getServerInfo() {
        return "Response from User MCP Server (Port: " + port + ")";
    }

    @PostMapping("/create_user")
    public User createUser(@RequestBody User user) throws Exception {
      return userTools.createUser(user);
    }

    @GetMapping("/get_user_info_by_login")
    public User getUserInfo(@RequestParam String login) {
      return userTools.getUserInfo(login);
    }

    @GetMapping("/get_users_info_by_email")
    public List<User> getUsersInfo(@RequestParam String email) {
      return userTools.getUsersInfo(email);
    }


}
