"""
Pydantic models for API request and response validation.
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    
    message: str = Field(
        ...,
        description="The user's question or message",
        min_length=1,
        examples=["What is the capital of France?"]
    )
    session_id: str = Field(
        default="default",
        description="Session ID for maintaining conversation context",
        examples=["user-123", "session-abc"]
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    
    response: str = Field(
        ...,
        description="The agent's response to the user's message"
    )
    session_id: str = Field(
        ...,
        description="Session ID used for this conversation"
    )


# Export models
__all__ = ["ChatRequest", "ChatResponse"]
