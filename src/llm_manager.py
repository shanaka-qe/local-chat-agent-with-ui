"""
LLM Manager for handling Ollama model initialization and configuration.
This module creates a LangChain wrapper around the local Ollama model.
"""

import ollama
from langchain_ollama import OllamaLLM
from config.settings import OLLAMA_MODEL, OLLAMA_BASE_URL, get_model_config

class LLMManager:
    """
    Manages the local Ollama model and provides a LangChain interface.
    This class handles all interactions with the local Llama model.
    """
    
    def __init__(self, model_name=None):
        """
        Initialize the LLM Manager with a specific model.
        
        Args:
            model_name (str): Name of the Ollama model to use. If None, uses default from config.
        """
        # Use the provided model name or fall back to the config default
        self.model_name = model_name or OLLAMA_MODEL
        
        # Get model configuration settings
        self.model_config = get_model_config()
        
        # Initialize the Ollama client
        # This client will communicate with the local Ollama server
        self.ollama_client = ollama.Client(host=OLLAMA_BASE_URL)
        
        # Create the LangChain Ollama wrapper
        # This allows us to use the local model with LangChain's interface
        self.llm = OllamaLLM(
            model=self.model_name,
            base_url=OLLAMA_BASE_URL,
            temperature=self.model_config["temperature"],
            top_p=self.model_config["top_p"]
        )
    
    def check_model_availability(self):
        """
        Check if the specified model is available in Ollama.
        
        Returns:
            bool: True if model is available, False otherwise
        """
        try:
            # Fast, precise check (preferred): ask Ollama for this model specifically
            # Works on recent Ollama clients/servers
            info = self.ollama_client.show(self.model_name)
            if isinstance(info, dict) and info:
                print(f"✓ Model '{self.model_name}' is available")
            return True
        except Exception as e:
            # Fall through to list-based check
            pass

        try:
            # Fallback: list all models and check by name
            models = self.ollama_client.list() or {}
            raw_models = models.get("models", [])
            model_names = []
            for m in raw_models:
                if isinstance(m, dict):
                    # Some versions expose 'name', others 'model'
                    n = m.get("name") or m.get("model") or ""
                    if n:
                        model_names.append(n)

            if self.model_name in model_names:
                print(f"✓ Model '{self.model_name}' is available")
                return True

            print(f"✗ Model '{self.model_name}' not found")
            print(f"Available models: {model_names}")
            return False

        except Exception as e:
            print(f"✗ Error checking model availability: {e}")
            print("Make sure Ollama is running (ollama serve)")
            return False

    
    def get_model_info(self):
        """
        Get information about the current model.
        This helps with debugging and understanding what model we're using.
        
        Returns:
            dict: Model information including name and configuration
        """
        return {
            "model_name": self.model_name,
            "base_url": OLLAMA_BASE_URL,
            "config": self.model_config
        }
    
    def test_model(self, test_prompt="Hello, how are you?"):
        """
        Test the model with a simple prompt.
        This is useful for verifying that everything is working correctly.
        
        Args:
            test_prompt (str): Simple prompt to test the model
            
        Returns:
            str: Model's response to the test prompt
        """
        try:
            # Use the LangChain interface to get a response
            response = self.llm.invoke(test_prompt)
            return response
        except Exception as e:
            return f"Error testing model: {e}"
    
    def get_llm(self):
        """
        Get the LangChain LLM object.
        This is used by other parts of the application to interact with the model.
        
        Returns:
            Ollama: The configured LangChain Ollama object
        """
        return self.llm
    
    @staticmethod
    def get_available_models():
        """
        Get list of all available Ollama models.
        This is a static method so it can be called without creating an LLMManager instance.
        
        Returns:
            list: List of available model names
        """
        try:
            # Use already imported ollama module
            client = ollama.Client()
            models = client.list()
            
            if models and 'models' in models:
                return [model.model for model in models['models'] if hasattr(model, 'model')]
            return []
            
        except Exception as e:
            print(f"Error getting available models: {e}")
            return []