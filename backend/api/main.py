"""FastAPI application for the Oracle of Delphi."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.models import ChatRequest, ChatResponse
from agent.graph import chat_with_state

load_dotenv()

app = FastAPI(
    title="Oracle of Delphi",
    description="An AI oracle with prophetic responses and ritual pacing",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API information."""
    return {
        "name": "Oracle of Delphi",
        "version": "1.0.0",
        "endpoints": {"/chat": "POST", "/health": "GET", "/docs": "GET"},
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Consult the Oracle."""
    try:
        if not os.getenv("GROQ_API_KEY"):
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not found.")
        
        response_text, ritual_state = chat_with_state(request.message, request.session_id)
        
        return ChatResponse(
            response=response_text,
            session_id=request.session_id,
            ritual_state=ritual_state
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
