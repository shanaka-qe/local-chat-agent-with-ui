"""
ChainLit UI for the LangChain Chatbot with Model Selection Dropdown.
This file creates a web interface for your existing chatbot.

Author: Shanaka Navaratne
"""
import os
import chainlit as cl
from chainlit.input_widget import Select
from langsmith import Client
from src.llm_manager import LLMManager
from src.chatbot import Chatbot
from config.settings import validate_config_silent, LANGSMITH_API_KEY, LANGSMITH_PROJECT

# Setup LangSmith tracing on module load
# This enables monitoring of all LLM interactions in the UI
def setup_langsmith():
    """
    Set up LangSmith tracing for monitoring LLM calls.
    This allows us to track and analyze all interactions with the language model.
    """
    # Check if LangSmith API key is available
    if not LANGSMITH_API_KEY:
        print("⚠️  LangSmith API key not found. Tracing will be disabled.")
        return False
    
    try:
        # Initialize LangSmith client
        # This client will send trace data to LangSmith for monitoring
        client = Client(api_key=LANGSMITH_API_KEY)
        
        # Set the project name for organizing traces
        # All traces from this session will be grouped under this project
        os.environ["LANGCHAIN_PROJECT"] = LANGSMITH_PROJECT
        
        print(f"✓ LangSmith tracing enabled for project: {LANGSMITH_PROJECT}")
        return True
        
    except Exception as e:
        print(f"✗ Error setting up LangSmith: {e}")
        return False

# Initialize LangSmith when the module loads
setup_langsmith()

@cl.on_chat_start
async def start():
    """
    Initialize the chatbot when a new chat session starts.
    """
    # Validate configuration
    if not validate_config_silent():
        await cl.Message(content="❌ Configuration validation failed. Please check your .env file.").send()
        return
    
    # Get available models using LLMManager
    available_models = LLMManager.get_available_models()
    if not available_models:
        await cl.Message(content="❌ No models found. Please install some models with 'ollama pull <model_name>'").send()
        return
    
    # Create dropdown for model selection in settings
    model_selector = Select(
        id="model_selector",
        label="Choose a Model",
        values=available_models,
        initial_index=0
    )
    
    # Send the settings with dropdown
    await cl.ChatSettings([model_selector]).send()
    
    # Initialize with the first model by default
    await initialize_chatbot(available_models[0])
    
    # Show available commands
    await cl.Message(content="🤖 Welcome! Select a model from the settings panel (⚙️) to get started, or continue with the default model.").send()
    await cl.Message(content="💡 **Available Commands:**\n- Type 'clear' to reset conversation memory\n- Type 'memory' to see conversation history\n- Type 'switch model' to change models\n- Type 'model info' to see current model details\n- Type 'test model' to test the current model").send()

async def initialize_chatbot(model_name):
    """
    Initialize the chatbot with the selected model.
    """
    try:
        # Initialize LLM manager with selected model
        llm_manager = LLMManager(model_name=model_name)
        
        # Check if model is available
        if not llm_manager.check_model_availability():
            await cl.Message(content=f"❌ Model '{model_name}' not available. Please check your Ollama installation.").send()
            return
        
        # Create chatbot with selected model (uses your full Chatbot class)
        chatbot = Chatbot(llm_manager)
        
        # Create a consistent session ID for this user session
        # Use ChainLit's session ID or create a unique one
        session_id = cl.user_session.get("id") or cl.context.session.id
        
        # Store in user session
        cl.user_session.set("chatbot", chatbot)
        cl.user_session.set("llm_manager", llm_manager)
        cl.user_session.set("current_model", model_name)
        cl.user_session.set("session_id", session_id)  # Store session ID
        
        # Send confirmation with model details
        model_info = llm_manager.get_model_info()
        await cl.Message(content=f"✅ **Model Initialized:** {model_name}").send()
        await cl.Message(content=f"🔧 **Model Configuration:**\n- Temperature: {model_info['config']['temperature']}\n- Top P: {model_info['config']['top_p']}\n- Base URL: {model_info['base_url']}").send()
        await cl.Message(content="🤖 Ready to chat! How can I help you today?").send()
        
    except Exception as e:
        await cl.Message(content=f"❌ Error initializing model '{model_name}': {e}").send()

@cl.on_settings_update
async def setup_agent(settings):
    """
    Handle model selection from dropdown.
    """
    selected_model = settings["model_selector"]
    current_model = cl.user_session.get("current_model")
    
    if selected_model != current_model:
        await cl.Message(content=f"🔄 Switching to model: {selected_model}").send()
        
        # Get existing chatbot to preserve conversation history
        chatbot = cl.user_session.get("chatbot")
        
        # Initialize new LLM manager
        llm_manager = LLMManager(model_name=selected_model)
        
        if not llm_manager.check_model_availability():
            await cl.Message(content=f"❌ Model '{selected_model}' not available.").send()
            return
        
        # Update the chatbot's LLM without losing conversation history
        if chatbot:
            chatbot.llm_manager = llm_manager
            chatbot.llm = llm_manager.get_llm()
            # Recreate the conversation chain with the new LLM
            chatbot.conversation_chain = chatbot._create_conversation_chain()
        
        # Store updated manager and model
        cl.user_session.set("llm_manager", llm_manager)
        cl.user_session.set("current_model", selected_model)
        
        await cl.Message(content=f"✅ Switched to {selected_model}. Conversation history preserved!").send()

@cl.on_message
async def main(message: cl.Message):
    """
    Handle each user message and get the chatbot response.
    """
    # Get chatbot from session
    chatbot = cl.user_session.get("chatbot")
    if not chatbot:
        await cl.Message(content="❌ Please select a model from the settings panel first.").send()
        return
    
    user_input = message.content.strip()
    
    # Get the session ID for this user (stored during initialization)
    session_id = cl.user_session.get("session_id", "default")
    
    # Check for UI-specific commands first
    if user_input.lower() in ['switch model', 'change model', '/switch']:
        await show_model_switcher()
        return
        
    elif user_input.lower() in ['model info', 'info']:
        await show_model_info()
        return
        
    elif user_input.lower() in ['test model', 'test']:
        await test_current_model()
        return
    
    # Use Chatbot's centralized command handler for chat commands
    command_response = chatbot.handle_command(user_input, session_id=session_id)
    if command_response:
        await cl.Message(content=command_response).send()
        return
    
    # Use existing chat logic with full conversation memory and chaining
    # Use ChainLit's session ID for proper conversation tracking
    try:
        response = chatbot.chat(user_input, session_id=session_id)
        await cl.Message(content=response).send()
    except Exception as e:
        await cl.Message(content=f"❌ Error: {e}").send()

async def show_model_info():
    """
    Show detailed information about the current model using LLMManager.
    """
    llm_manager = cl.user_session.get("llm_manager")
    
    if not llm_manager:
        await cl.Message(content="❌ No model manager found. Please select a model first.").send()
        return
    
    # Get model information using LLMManager.get_model_info()
    model_info = llm_manager.get_model_info()
    
    await cl.Message(content=f"📊 **Model Information:**").send()
    await cl.Message(content=f"**Model Name:** {model_info['model_name']}").send()
    await cl.Message(content=f"**Base URL:** {model_info['base_url']}").send()
    await cl.Message(content=f"**Temperature:** {model_info['config']['temperature']}").send()
    await cl.Message(content=f"**Top P:** {model_info['config']['top_p']}").send()
    
    # Test model availability using LLMManager.check_model_availability()
    is_available = llm_manager.check_model_availability()
    status = "✅ Available" if is_available else "❌ Not Available"
    await cl.Message(content=f"**Status:** {status}").send()

async def test_current_model():
    """
    Test the current model using LLMManager.test_model().
    """
    llm_manager = cl.user_session.get("llm_manager")
    
    if not llm_manager:
        await cl.Message(content="❌ No model manager found. Please select a model first.").send()
        return
    
    await cl.Message(content="🧪 **Testing current model...**").send()
    
    try:
        # Use LLMManager.test_model() method
        test_response = llm_manager.test_model("Hello! Please respond with a brief greeting to test the model.")
        await cl.Message(content=f"✅ **Model Test Response:**\n{test_response}").send()
    except Exception as e:
        await cl.Message(content=f"❌ **Model Test Failed:** {e}").send()

async def show_model_switcher():
    """
    Show model selection interface using LLMManager.
    """
    # Use LLMManager to get available models
    available_models = LLMManager.get_available_models()
    current_model = cl.user_session.get("current_model", "Unknown")
    llm_manager = cl.user_session.get("llm_manager")
    
    await cl.Message(content=f"🔄 **Current model:** {current_model}").send()
    
    # Use LLMManager to check model status
    if llm_manager:
        is_available = llm_manager.check_model_availability()
        status = "✅ Available" if is_available else "❌ Not Available"
        await cl.Message(content=f"**Status:** {status}").send()
    
    await cl.Message(content=f"**Available models:** {', '.join(available_models)}").send()
    await cl.Message(content="💡 Use the settings panel (⚙️) to switch models, or type a model name to switch directly.").send()
    
    # Show model comparison
    if len(available_models) > 1:
        await cl.Message(content="💡 **Tip:** You can compare different models by switching between them. Each model has different capabilities and response styles.").send()