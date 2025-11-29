"""
LangGraph agent implementation with tool calling and memory.
This module creates a state graph that manages conversation flow,
determines when to use tools, and maintains conversation context.
"""

import os
from typing import Annotated, TypedDict, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from agent.tools import search_facts


# Define the state structure
class AgentState(TypedDict):
    """State of the agent containing messages and conversation context."""
    messages: Annotated[Sequence[BaseMessage], add_messages]


# Initialize the LLM with tools
def create_agent():
    """
    Create and configure the LangGraph agent with tools and memory.
    
    Returns:
        A compiled LangGraph application with checkpointing for memory.
    """
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in environment variables. "
            "Please set it in your .env file or environment."
        )
    
    # Initialize the LLM
    llm = ChatGroq(
        model="mixtral-8x7b-32768",  # Fast and capable model
        temperature=0.7,
        api_key=api_key,
    )
    
    # Bind tools to the LLM
    tools = [search_facts]
    llm_with_tools = llm.bind_tools(tools)
    
    # Define the agent node
    def call_model(state: AgentState) -> dict:
        """
        Node that calls the LLM with the current conversation state.
        The LLM will decide whether to use tools or respond directly.
        """
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    # Define routing logic
    def should_continue(state: AgentState) -> str:
        """
        Determine whether to continue to tools or end the conversation.
        
        Returns:
            "tools" if the LLM wants to use a tool, otherwise "end"
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        # If there are tool calls, continue to tools node
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        
        # Otherwise, end the conversation turn
        return "end"
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("llm_node", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    # Set the entry point
    workflow.set_entry_point("llm_node")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "llm_node",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )
    
    # Add edge from tools back to llm_node
    workflow.add_edge("tools", "llm_node")
    
    # Initialize checkpointer for memory (using in-memory saver)
    memory = MemorySaver()
    
    # Compile the graph with checkpointing
    app = workflow.compile(checkpointer=memory)
    
    return app


# Create a singleton instance
_agent_app = None


def get_agent():
    """
    Get the singleton agent instance.
    Creates the agent on first call and reuses it afterwards.
    """
    global _agent_app
    if _agent_app is None:
        _agent_app = create_agent()
    return _agent_app


def chat(message: str, session_id: str = "default") -> str:
    """
    Send a message to the agent and get a response.
    
    Args:
        message: The user's message
        session_id: Unique identifier for the conversation session (for memory)
        
    Returns:
        The agent's response as a string
    """
    app = get_agent()
    
    # Create the config with thread_id for memory persistence
    config = {"configurable": {"thread_id": session_id}}
    
    # Invoke the agent
    result = app.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=config
    )
    
    # Extract the final response
    final_message = result["messages"][-1]
    return final_message.content


# Export functions
__all__ = ["create_agent", "get_agent", "chat"]
