# AI Question-Answer Helper 🤖

A simple AI agent built with LangGraph that intelligently answers user questions, uses a dictionary-based search tool for factual queries, and maintains conversation memory.

## ✨ Features

- **Intelligent Tool Use**: Automatically detects factual questions and uses the search tool
- **Conversational AI**: Provides natural responses for general questions
- **Memory**: Maintains conversation context using session-based memory
- **REST API**: FastAPI-based HTTP endpoint for easy integration
- **LangGraph**: State machine architecture for robust agent behavior

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│  FastAPI    │
│  /chat      │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│    LangGraph Agent          │
│  ┌─────────┐                │
│  │  Agent  │ ◄──────┐       │
│  └────┬────┘        │       │
│       │             │       │
│       ▼             │       │
│  Should use tool?   │       │
│    ┌─Yes───No       │       │
│    │      │         │       │
│    ▼      ▼         │       │
│  ┌────┐  End ───────┘       │
│  │Tool│                     │
│  └────┘                     │
│    │                        │
│    └─► SQLite Memory        │
└─────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key ([Get one here](https://console.groq.com/keys))

### Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Groq API key
   # GROQ_API_KEY=your_actual_api_key_here
   ```

### Running the Server

```bash
uvicorn api.main:app --reload --port 8000
```

The server will start at `http://localhost:8000`

## 📖 API Usage

### Chat Endpoint

**POST** `/chat`

Send a message to the AI agent and receive a response.

#### Request Body

```json
{
  "message": "What is the capital of France?",
  "session_id": "user-123"
}
```

#### Response

```json
{
  "response": "The capital of France is Paris.",
  "session_id": "user-123"
}
```

### Example with curl

```bash
# Factual question (uses search tool)
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"What is the capital of Japan?\", \"session_id\": \"test\"}"

# Conversational question
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Hello! How are you?\", \"session_id\": \"test\"}"
```

### Example with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "What is the speed of light?",
        "session_id": "my-session"
    }
)

print(response.json()["response"])
```

## 🧪 Testing

### Direct Agent Testing

Run the test script to test the agent directly without the API:

```bash
python test_agent.py
```

This will test:
- Factual questions that should trigger the search tool
- Conversational questions that should get direct responses
- Memory/context maintenance across messages

### Interactive API Testing

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## 📂 Project Structure

```
.
├── agent/
│   ├── __init__.py
│   ├── tools.py          # Dictionary-based search tool
│   └── graph.py          # LangGraph agent logic
├── api/
│   ├── __init__.py
│   ├── models.py         # Pydantic request/response models
│   └── main.py           # FastAPI application
├── test_agent.py         # Test script
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── .gitignore
└── README.md
```

## 🔧 How It Works

### 1. Tool System
The `search_facts` tool contains a knowledge base with:
- Country capitals
- Population data
- Science facts
- Technology definitions

### 2. Agent Logic
The LangGraph agent:
1. Receives user message
2. Uses LLM to determine if a tool is needed
3. Calls the search tool if needed, or responds directly
4. Maintains conversation history in SQLite

### 3. Memory
- **Session-based**: Each `session_id` has separate conversation memory
- **Persistent**: Uses SQLite checkpointing (in-memory by default)
- **Context-aware**: Agent remembers previous messages in the session

## 🎯 Example Interactions

### Factual Query
```
User: "What is the capital of Germany?"
Agent: "The capital of Germany is Berlin."
[Uses search tool]
```

### Conversational
```
User: "Hello! How are you?"
Agent: "Hello! I'm doing great, thank you for asking! How can I help you today?"
[Direct response, no tool]
```

### With Memory
```
User: "What is the capital of France?"
Agent: "The capital of France is Paris."

User: "What about its population?"
Agent: "The population of Paris is approximately 2.2 million..."
[Remembers "its" refers to Paris]
```

## 🛠️ Customization

### Adding More Facts
Edit `agent/tools.py` and add entries to the `KNOWLEDGE_BASE` dictionary:

```python
KNOWLEDGE_BASE = {
    "capital": {
        "your_country": "Your Capital",
        # Add more...
    },
    # Add more categories...
}
```

### Changing the LLM
Edit `agent/graph.py` to use a different model:

```python
llm = ChatGroq(
    model="llama3-70b-8192",  # Different model
    temperature=0.5,          # Adjust temperature
)
```

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |

## 🐛 Troubleshooting

**Error: "GROQ_API_KEY not found"**
- Make sure you've created a `.env` file with your API key
- Check that the `.env` file is in the project root directory

**Agent not using the search tool**
- The LLM decides whether to use tools based on the query
- Try more specific factual questions like "What is the capital of X?"

**Memory not working**
- Ensure you're using the same `session_id` for related messages
- Memory is stored in-memory by default and resets when server restarts

## 📚 Learn More

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq Documentation](https://console.groq.com/docs)

## 🙏 Acknowledgments

Built with:
- **LangGraph** for agent orchestration
- **FastAPI** for the REST API
- **Groq** for fast LLM inference
- **LangChain** for tool integration

---

Happy coding! 🚀
