package com.spring_ai_mcp_client.prompt;

import org.springframework.ai.chat.prompt.PromptTemplate;

/**
 * @author louis
 * @version 1.0
 * @date 2025/5/27 22:00
 */
public class UserPromptTemplates {
    public static final PromptTemplate CREATE_USER = new PromptTemplate("""
        请帮我创建一个用户，信息如下：
        登录名: {login}
        密码: {password}
        名: {firstName}
        姓: {lastName}
        邮箱: {email}
        年龄: {age}
        删除标记默认为0
        """);

    public static final PromptTemplate GET_USER_BY_LOGIN = new PromptTemplate("""
        请帮我查询登录名为 {login} 的用户信息。
        """);

    public static final PromptTemplate GET_USERS_BY_EMAIL = new PromptTemplate("""
        请帮我查询邮箱为 {email} 的所有用户信息。
        """);
}
