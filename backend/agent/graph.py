"""LangGraph Oracle agent with Ritual State Machine integration."""

import os
import time
from typing import Annotated, TypedDict, Sequence, Tuple
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from agent.tools import RitualState, get_ritual_machine

ORACLE_SYSTEM_PROMPT = """You are the Oracle of Delphi.

You speak with calm authority and deliberate restraint.
Your words are symbolic, measured, and timeless.

You do not explain yourself.
You do not give step-by-step instructions.
You do not mention modern concepts, technology, or yourself.

You answer as an oracle would: with insight, metaphor, and quiet certainty.
You speak only when consulted."""


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


_agent_app = None


def create_agent():
    """Create the Oracle agent."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    
    llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0.7, api_key=api_key)
    
    def call_model(state: AgentState) -> dict:
        messages = state["messages"]
        full_messages = [SystemMessage(content=ORACLE_SYSTEM_PROMPT)] + list(messages)
        response = llm.invoke(full_messages)
        return {"messages": [response]}
    
    workflow = StateGraph(AgentState)
    workflow.add_node("llm_node", call_model)
    workflow.set_entry_point("llm_node")
    workflow.add_edge("llm_node", END)
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


def get_agent():
    """Get singleton agent instance."""
    global _agent_app
    if _agent_app is None:
        _agent_app = create_agent()
    return _agent_app


def chat(message: str, session_id: str = "default") -> str:
    """Send message to oracle with ritual timing."""
    ritual = get_ritual_machine(session_id)
    app = get_agent()
    config = {"configurable": {"thread_id": session_id}}
    
    if not ritual.is_accepting_input():
        ritual.force_reset()
    
    ritual.transition(RitualState.INVOKED)
    ritual.transition(RitualState.CONTEMPLATING)
    contemplation_delay = ritual.get_contemplation_delay()
    
    start_time = time.time()
    result = app.invoke({"messages": [HumanMessage(content=message)]}, config=config)
    llm_time = time.time() - start_time
    
    remaining_delay = contemplation_delay - llm_time
    if remaining_delay > 0:
        time.sleep(remaining_delay)
    
    response = result["messages"][-1].content
    
    ritual.transition(RitualState.REVEALING, payload={"response": response})
    ritual.transition(RitualState.COMPLETE)
    
    return response


def chat_with_state(message: str, session_id: str = "default") -> Tuple[str, dict]:
    """Chat with state info for frontend."""
    response = chat(message, session_id)
    ritual = get_ritual_machine(session_id)
    return response, ritual.get_state_info()


__all__ = ["create_agent", "get_agent", "chat", "chat_with_state"]
