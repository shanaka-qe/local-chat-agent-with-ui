"""
Chatbot implementation using LangChain with conversation memory.
This module handles the conversation logic and maintains context across messages.
"""
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from config.settings import SYSTEM_MESSAGE

class Chatbot:
    """
    A conversational chatbot that maintains context across multiple messages.
    This class handles the conversation flow and memory management.
    """
    
    def __init__(self, llm_manager):
        """
        Initialize the Chatbot with a language model manager.
        
        Args:
            llm_manager (LLMManager): The LLM manager that provides the language model
        """
        # Store the LLM manager for accessing the language model
        self.llm_manager = llm_manager
        
        # Get the LangChain LLM object from the manager
        self.llm = llm_manager.get_llm()
        
        # Create conversation memory to maintain context using modern history API
        # Keep per-session histories in an in-memory store
        self._memory_store = {}
        
        # Create the conversation chain (LLM + prompt) wrapped with message history
        self.conversation_chain = self._create_conversation_chain()
    

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """
        Retrieve or create a chat history object for a given session id.
        """
        history = self._memory_store.get(session_id)
        if history is None:
            history = ChatMessageHistory()
            self._memory_store[session_id] = history
        return history
    

    def chat(self, user_input, session_id="default"):
        """
        Process user input and return the chatbot's response.
        This is the main method for interacting with the chatbot.
        
        Args:
            user_input (str): The user's message
            session_id (str): Session identifier for conversation history
            
        Returns:
            str: The chatbot's response
        """
        try:
            # RunnableWithMessageHistory requires config with session_id
            config = {"configurable": {"session_id": session_id}}
            
            # Invoke with proper config - RunnableWithMessageHistory handles the rest
            response = self.conversation_chain.invoke(
                {"input": user_input},
                config=config
            )
            
            return getattr(response, "content", response)
        except Exception as e:
            print(f"[ERROR] Chat error: {e}")
            import traceback
            traceback.print_exc()
            return f"Sorry, I encountered an error: {e}"
    
    def clear_memory(self, session_id="default"):
        """
        Clear the conversation memory for a specific session.
        This starts a fresh conversation without any previous context.
        
        Args:
            session_id (str): Session identifier to clear memory for
        """
        # Clear specific session or all sessions
        if session_id in self._memory_store:
            del self._memory_store[session_id]
            print(f"Conversation memory cleared for session: {session_id}")
        else:
            self._memory_store.clear()
            print("All conversation memory cleared. Starting fresh conversation.")
    
    def get_memory_summary(self, session_id="default"):
        """
        Get a summary of the current conversation memory for a specific session.
        This is useful for debugging and understanding what the chatbot remembers.
        
        Args:
            session_id (str): Session identifier to get memory for
            
        Returns:
            str: Summary of the conversation history
        """
        # Get the conversation history from memory
        history = self.get_session_history(session_id)
        messages = getattr(history, "messages", [])

        if not messages:
            return "No conversation history yet."
        
        # Format the conversation history for display
        summary = "Recent conversation:\n"
        for i, message in enumerate(messages[-6:], 1):  # Show last 6 messages
            role = "Human" if isinstance(message, HumanMessage) else "AI"
            content = message.content[:100] + "..." if hasattr(message, "content") and len(message.content) > 100 else getattr(message, "content", "")
            summary += f"{i}. {role}: {content}\n"
        
        return summary
    
    def handle_command(self, user_input, session_id="default"):
        """
        Handle special commands and return appropriate response.
        Returns None if it's not a command, otherwise returns the command response.
        
        Args:
            user_input (str): The user's input
            session_id (str): Session identifier for conversation history
            
        Returns:
            str or None: Command response if it's a command, None if it's regular chat
        """
        user_input = user_input.strip().lower()
        
        if user_input in ['clear']:
            self.clear_memory(session_id)
            return "🧹 Conversation memory cleared. Starting fresh conversation."
            
        elif user_input in ['memory']:
            return f"📝 **Conversation Memory:**\n{self.get_memory_summary(session_id)}"
            
        # Return None if it's not a command (regular chat message)
        return None

    def _create_conversation_chain(self):
        """
        Create the LangChain runnable chain with message history.
        Combines the LLM, a chat prompt, and per-session history.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_MESSAGE),
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])

        core_chain = prompt | self.llm

        runnable_with_history = RunnableWithMessageHistory(
            core_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return runnable_with_history
        