from langchain.tools import Tool
from langchain_community.llms import Ollama
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = Ollama(
    base_url="http://localhost:11434",
    model="deepseek-r1:7b",
    temperature=0.7,
    verbose=True  # Enable verbose logging
)

def general_chat(query: str) -> str:
    """General chat tool for handling general questions and conversations"""
    try:
        logger.info(f"Calling Ollama model to process query: {query[:50]}...")
        
        # Use modern invoke method
        response = llm.invoke(query)
        
        # Clean response content, remove <think> tags
        cleaned_response = clean_response(response)
        
        logger.info(f"Ollama response completed, length: {len(cleaned_response)} characters")
        return cleaned_response
        
    except Exception as e:
        error_msg = f"Chat processing failed: {e}"
        logger.error(error_msg)
        return error_msg

def clean_response(response: str) -> str:
    """Clean response content, remove think tags and extra whitespace"""
    if not response:
        return "Sorry, I didn't generate a response."
    
    # Remove <think> tags and their content
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    
    # Remove extra blank lines
    response = re.sub(r'\n\s*\n', '\n\n', response)
    
    # Strip leading and trailing whitespace
    response = response.strip()
    
    # If empty after cleaning, return default message
    if not response:
        return "I understand your question, but I can't provide a suitable answer at the moment. Please try asking in a different way."
    
    return response

chat_tool = Tool(
    name="general_chat",
    func=general_chat,
    description="General conversation, knowledge Q&A, telling jokes, etc."
) 