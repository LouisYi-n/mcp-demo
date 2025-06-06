package com.user_mcp_server.repository;

import com.user_mcp_server.model.User;
import com.user_mcp_server.model.UserDTO;
import java.util.List;
import org.springframework.data.repository.CrudRepository;

public interface UserRepository extends CrudRepository<User, Long> {
    List<User> findUsersByEmail(String email);

    User findUserByLogin(String login);

    UserDTO save(UserDTO user);
}
