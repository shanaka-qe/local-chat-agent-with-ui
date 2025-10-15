# 📖 User Guide: Local Chat Agent with Multi-Model Support

Welcome to the Local Chat Agent! This comprehensive guide will walk you through everything you need to know to set up, configure, and use your local AI chatbot with multiple model support.

## 📋 Table of Contents

1. [What is this project?](#what-is-this-project)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Using the Chat Interface](#using-the-chat-interface)
7. [Multi-Model Features](#multi-model-features)
8. [Commands Reference](#commands-reference)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

## What is this project?

This is a **local AI chatbot** that runs entirely on your computer using Ollama models. It features:

- 🤖 **Multiple AI Models**: Switch between different models (Llama, Gemma, Mistral, etc.)
- 💬 **Conversation Memory**: Remembers your chat history
- 🎨 **Modern Web Interface**: Clean, ChatGPT-like interface
- 🔒 **Complete Privacy**: Everything runs locally on your machine
- 📊 **Optional Monitoring**: LangSmith integration for debugging

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **Python**: Version 3.10 or higher
- **RAM**: 8GB minimum (16GB recommended for larger models)
- **Storage**: 10GB free space for models
- **Internet**: Required only for initial model downloads

### Recommended Setup
- **RAM**: 16GB+ for smooth operation with multiple models
- **Storage**: 50GB+ for multiple large models
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster inference)

## Installation Guide

### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://python.org)
2. Run the installer and check "Add Python to PATH"
3. Verify installation: Open Command Prompt and run `python --version`

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
# Verify installation
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Install Ollama

**macOS:**
```bash
# Using Homebrew (recommended)
brew install ollama

# Or download from ollama.ai
```

**Windows:**
1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Ollama will be added to your PATH automatically

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 3: Download AI Models

Start Ollama and download some models:

```bash
# Start Ollama service
ollama serve

# In a new terminal, download models
ollama pull gemma3:4b      # Fast, efficient model (4GB)
ollama pull llama3:latest  # High-quality model (8GB)
ollama pull mistral:latest # Alternative model (4GB)
ollama pull codellama:latest # Code-focused model (4GB)
```

**Model Size Guide:**
- **Small models (4GB)**: Fast responses, good for testing
- **Medium models (8GB)**: Balanced performance and quality
- **Large models (13GB+)**: Best quality, requires more RAM

### Step 4: Set Up the Project

1. **Clone or download the project:**
```bash
git clone <your-repo-url>
cd local-chat-agent-with-ui
```

2. **Create a virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Configuration

### Basic Configuration

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env  # On Windows: type nul > .env
```

Add the following content to `.env`:

```env
# Ollama Configuration
OLLAMA_MODEL=gemma3:4b
OLLAMA_BASE_URL=http://localhost:11434

# LangSmith Configuration (Optional)
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=langchain-chatbot
```

### Advanced Configuration

You can customize the chatbot behavior by modifying `config/settings.py`:

```python
# Model behavior settings
MODEL_TEMPERATURE = 0.7    # 0 = deterministic, 1 = very random
MAX_TOKENS = 1000         # Maximum response length
TOP_P = 0.9              # Response diversity

# Chat settings
MAX_MEMORY_SIZE = 10     # Conversation turns to remember
```

### LangSmith Setup (Optional)

LangSmith provides monitoring and debugging for your AI conversations:

1. **Sign up at [smith.langchain.com](https://smith.langchain.com)**
2. **Get your API key** from the dashboard
3. **Add to your `.env` file:**
```env
LANGSMITH_API_KEY=your_actual_api_key_here
LANGSMITH_PROJECT=my-chatbot-project
```

## Running the Application

### Start the Chat Interface

1. **Make sure Ollama is running:**
```bash
ollama serve
```

2. **Activate your virtual environment:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Start the application:**
```bash
chainlit run ui_app.py
```

4. **Open your browser** and go to: `http://localhost:8000`

### First Launch Checklist

- ✅ Ollama is running (`ollama serve`)
- ✅ At least one model is downloaded (`ollama list`)
- ✅ Virtual environment is activated
- ✅ Dependencies are installed
- ✅ Browser opens to `http://localhost:8000`

## Using the Chat Interface

### Getting Started

1. **Select a Model**: Use the settings panel (⚙️) to choose your preferred model
2. **Start Chatting**: Type your message and press Enter
3. **View Responses**: The AI will respond in real-time

### Interface Overview

- **💬 Chat Area**: Where conversations happen
- **⚙️ Settings Panel**: Model selection and configuration
- **📝 Message Input**: Type your questions here
- **🔄 Model Switcher**: Change models without losing context

### Basic Chat Commands

Type these commands in the chat:

| Command | Description | Example |
|---------|-------------|---------|
| `clear` | Reset conversation memory | Type "clear" to start fresh |
| `memory` | View conversation history | Type "memory" to see chat history |
| `model info` | Show current model details | Type "model info" for model stats |
| `test model` | Test model connection | Type "test model" to verify setup |
| `switch model` | Show model switching options | Type "switch model" for help |

## Multi-Model Features

### Dynamic Model Switching

**How to switch models:**
1. Click the settings icon (⚙️) in the interface
2. Select a different model from the dropdown
3. Continue your conversation - context is preserved!

**Benefits:**
- Compare different models on the same question
- Use specialized models for different tasks
- Switch between speed and quality

### Model Comparison Workflow

1. **Start with a fast model** (e.g., `gemma3:4b`)
2. **Ask your question** and get a quick response
3. **Switch to a high-quality model** (e.g., `llama3:latest`)
4. **Ask the same question** to compare responses
5. **Switch back** - your conversation history is preserved

### Specialized Use Cases

- **Code Generation**: Use `codellama` for programming tasks
- **General Chat**: Use `llama3` for comprehensive responses
- **Quick Responses**: Use `gemma3:4b` for fast answers
- **Creative Writing**: Use `mistral` for creative tasks

## Commands Reference

### Chat Commands

| Command | Function | Usage |
|---------|----------|-------|
| `clear` | Clears conversation memory | Start a fresh conversation |
| `memory` | Shows conversation history | Debug or review chat history |
| `model info` | Displays current model details | Check model configuration |
| `test model` | Tests model connectivity | Verify model is working |
| `switch model` | Shows model switching help | Get help with model switching |

### Model Management

**Check available models:**
```bash
ollama list
```

**Download new models:**
```bash
ollama pull model-name
```

**Remove models:**
```bash
ollama rm model-name
```

## Troubleshooting

### Common Issues and Solutions

#### "Model not available" Error
**Problem**: The selected model isn't found
**Solution**:
1. Check if Ollama is running: `ollama serve`
2. Verify model exists: `ollama list`
3. Download the model: `ollama pull model-name`

#### "No models found" Error
**Problem**: No models are installed
**Solution**:
```bash
# Download at least one model
ollama pull gemma3:4b
```

#### "ChainLit UI not loading"
**Problem**: Web interface won't start
**Solution**:
1. Check if port 8000 is available
2. Try a different port: `chainlit run ui_app.py --port 8001`
3. Verify ChainLit is installed: `pip install chainlit`

#### "Import errors"
**Problem**: Python dependencies missing
**Solution**:
1. Activate virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`

#### "Conversation history not working"
**Problem**: Chat doesn't remember previous messages
**Solution**:
1. Use the web interface (not terminal)
2. Ensure you're using a supported model
3. Check if the model supports conversation context

#### "Slow responses"
**Problem**: Model responses are very slow
**Solution**:
1. Use a smaller model (e.g., `gemma3:4b`)
2. Close other applications to free up RAM
3. Consider using a GPU-accelerated model

### Performance Optimization

**For faster responses:**
- Use smaller models (4GB instead of 8GB+)
- Close unnecessary applications
- Use SSD storage for models
- Consider GPU acceleration

**For better quality:**
- Use larger models (8GB+)
- Increase `MAX_TOKENS` in settings
- Adjust `MODEL_TEMPERATURE` for creativity

## Advanced Usage

### Custom Model Configuration

Edit `config/settings.py` to customize model behavior:

```python
# More creative responses
MODEL_TEMPERATURE = 0.9

# Longer responses
MAX_TOKENS = 2000

# More focused responses
TOP_P = 0.8
```

### Custom System Prompts

Modify the system message in `config/settings.py`:

```python
SYSTEM_MESSAGE = """You are a helpful coding assistant. 
You specialize in Python programming and provide clear, 
well-commented code examples. Always explain your reasoning."""
```

### Multiple User Sessions

The application supports multiple users simultaneously:
- Each user gets their own conversation history
- Model switching is per-user
- Sessions are isolated from each other

### LangSmith Monitoring

If you've set up LangSmith:
1. Visit [smith.langchain.com](https://smith.langchain.com)
2. View your project dashboard
3. Monitor conversation traces
4. Analyze model performance

### Backup and Restore

**Backup your configuration:**
```bash
# Copy your .env file
cp .env .env.backup

# Export your model list
ollama list > models.txt
```

**Restore configuration:**
```bash
# Restore .env file
cp .env.backup .env

# Reinstall models
cat models.txt | xargs -I {} ollama pull {}
```

## Getting Help

### Support Resources

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the README.md for technical details
- **Community**: Join AI/ML communities for help

### Useful Commands

```bash
# Check Ollama status
ollama ps

# View model details
ollama show model-name

# Update Ollama
ollama update

# Check Python version
python --version

# Check installed packages
pip list
```

---

## 🎉 Congratulations!

You now have a fully functional local AI chatbot with multi-model support! 

**Next Steps:**
1. Experiment with different models
2. Try the various chat commands
3. Customize the system prompts
4. Set up LangSmith monitoring
5. Explore advanced features

**Happy Chatting!** 🤖💬
