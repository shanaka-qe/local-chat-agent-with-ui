"""
Configuration settings for the LangChain Chatbot project.
This module handles loading environment variables and setting up project constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows us to store sensitive information like API keys in a separate file
load_dotenv()

# LangSmith configuration
# LangSmith is used for tracing and monitoring our LLM calls
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "langchain-chatbot")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

# Ollama configuration
# Ollama is the tool we use to run local Llama models
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Model configuration
# These settings control how the model behaves
MODEL_TEMPERATURE = 0.7  # Controls randomness: 0 = deterministic, 1 = very random
MAX_TOKENS = 1000  # Maximum number of tokens the model can generate
TOP_P = 0.9  # Controls diversity of responses

# Chat configuration
# These settings control the chatbot behavior
MAX_MEMORY_SIZE = 10  # Maximum number of conversation turns to remember
SYSTEM_MESSAGE = """You are a helpful AI assistant. 
You should be friendly, informative, and try to help the user with their questions.
Keep your responses simple and direct but complete."""

def validate_config_silent():
    """
    Validate configuration without printing messages.
    Useful for UI applications where you want to handle errors differently.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    return bool(OLLAMA_MODEL and OLLAMA_BASE_URL)

def get_model_config():
    """
    Get the model configuration as a dictionary.
    This makes it easy to pass configuration to the model.
    """
    return {
        "temperature": MODEL_TEMPERATURE,
        "top_p": TOP_P
    }
