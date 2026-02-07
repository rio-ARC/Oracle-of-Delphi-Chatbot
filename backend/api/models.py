"""Pydantic models for API validation."""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., min_length=1)
    session_id: str = Field(default="default")


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: str
    ritual_state: Optional[Dict[str, Any]] = None


__all__ = ["ChatRequest", "ChatResponse"]
