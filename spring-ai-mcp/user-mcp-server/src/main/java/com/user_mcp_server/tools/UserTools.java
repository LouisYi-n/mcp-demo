package com.user_mcp_server.tools;

import com.user_mcp_server.model.User;
import com.user_mcp_server.repository.UserRepository;
import java.util.List;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

/**
 * @author louis
 * @version 1.0
 * @date 2025/5/27 20:19
 */
@Service
public class UserTools {

    private final UserRepository userRepository;

    public UserTools(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Tool(description = "get Users info by login")
    public User getUserInfo(@ToolParam(description = "login") String login) {
        return userRepository.findUserByLogin(login);
    }

    @Tool(description = "create User")
    public User createUser(@ToolParam(description = "User") User user) throws Exception {
        String checkData = checkData(user);
        if (StringUtils.hasLength(checkData)) {
            throw new Exception("Invalid data." + checkData);
        }

        User checkUser = userRepository.findUserByLogin(user.getLogin());
        if (checkUser != null) {
            throw new Exception("User with login " + user.getLogin() + " already exists.");
        }

        return userRepository.save(user);
    }

   @Tool(description = "get Users info by email")
    public List<User> getUsersInfo(@ToolParam(description = "email") String email) {
        return userRepository.findUsersByEmail(email);
    }

    private String checkData(User user) {
        StringBuilder sb = new StringBuilder();
        if (user.getLogin() == null) {
            sb.append("login can not be empty;");
        }
        if (user.getPassword() == null) {
            sb.append("password can not be empty;");
        }
        if (user.getFirstName() == null) {
            sb.append("firstName can not be empty;");
        }
        if (user.getLastName() == null) {
            sb.append("lastName can not be empty;");
        }
        if (user.getEmail() == null) {
            sb.append("email can not be empty;");
        }


        return sb.toString();
    }
}
