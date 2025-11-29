"""
FastAPI application for the AI Question-Answer Helper.
Provides a REST API endpoint for chatting with the AI agent.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.models import ChatRequest, ChatResponse
from agent.graph import chat

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI Question-Answer Helper",
    description="A simple AI agent that answers questions and uses a search tool for factual queries",
    version="1.0.0",
)

# Add CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint providing API information.
    """
    return {
        "name": "AI Question-Answer Helper",
        "version": "1.0.0",
        "description": "A LangGraph-based AI agent with tool calling and memory",
        "endpoints": {
            "/chat": "POST - Send a message to the AI agent",
            "/docs": "GET - Interactive API documentation",
        },
        "features": [
            "Factual question answering using search tool",
            "Conversational responses for general questions",
            "Session-based conversation memory",
        ],
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat with the AI agent.
    
    The agent will:
    - Use the search tool for factual questions
    - Provide conversational responses for general questions
    - Maintain context within the same session_id
    
    Args:
        request: ChatRequest containing the message and optional session_id
        
    Returns:
        ChatResponse with the agent's response
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        # Check if API key is set
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY not found. Please set it in your .env file."
            )
        
        # Get response from agent
        response_text = chat(request.message, request.session_id)
        
        return ChatResponse(
            response=response_text,
            session_id=request.session_id
        )
        
    except ValueError as e:
        # Handle missing API key or configuration errors
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "message": "AI agent is ready"}


# Run with: uvicorn api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
