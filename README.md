# Oracle of Delphi 🏛️

An AI-powered oracle that speaks in prophecies, built with LangGraph, FastAPI, and vanilla JavaScript. Features ritualized response timing and an immersive Greek mythology theme.

**🔗 Live Demo:** [oracle-of-delphi-chatbot.vercel.app](https://oracle-of-delphi-chatbot.vercel.app/)

**⚙️ Backend API:** [oracle-delphi-api.onrender.com](https://oracle-delphi-api.onrender.com)

---

## ✨ Features

- **🔮 Prophetic Persona**: Oracle responds with metaphors and symbolic language, never mentioning modern concepts
- **⏳ Ritualized Timing**: 1.5-4 second contemplation delay before each response for gravitas
- **🧠 Session Memory**: Maintains conversation context within each browser session
- **🏛️ Immersive UI**: Greek temple background with parchment-style interface
- **⚡ Fast Inference**: Powered by Groq's LPU architecture (llama-3.3-70b-versatile)

---

## 🏗️ Architecture

```
┌──────────────────┐
│  Vercel Frontend │  (oracle-delphi/)
│  HTML/CSS/JS     │
└────────┬─────────┘
         │ HTTPS POST /chat
         ▼
┌──────────────────────────────────┐
│   Render Backend (FastAPI)       │
│  ┌────────────────────────────┐  │
│  │  Ritual State Machine      │  │
│  │  IDLE → INVOKED →          │  │
│  │  CONTEMPLATING → REVEALING │  │
│  └────────┬───────────────────┘  │
│           │                       │
│           ▼                       │
│  ┌────────────────────────────┐  │
│  │   LangGraph Oracle Agent   │  │
│  │   + Oracle System Prompt   │  │
│  └────────┬───────────────────┘  │
│           │                       │
│           ▼                       │
│      In-Memory Session Storage    │
└───────────┬───────────────────────┘
            │ API call
            ▼
    ┌──────────────┐
    │  Groq Cloud  │
    │  (LLM runs)  │
    └──────────────┘
```

---

## � How It Works

### 1. Ritual State Machine

Each oracle consultation flows through 5 states:

| State | Duration | Purpose |
|-------|----------|---------|
| **IDLE** | Indefinite | Awaiting question |
| **INVOKED** | <100ms | Question received |
| **CONTEMPLATING** | 1.5-4s (random) | Deliberate silence |
| **REVEALING** | Instant | Response delivered |
| **COMPLETE** | 2s | Ritual complete |

The contemplation delay runs **while** the LLM generates the response. If the LLM finishes early, the system waits for the contemplation timer to expire before revealing the response.

### 2. Oracle Persona

Every response is prefixed with this system prompt:

> *"You are the Oracle of Delphi. You speak with calm authority and deliberate restraint. Your words are symbolic, measured, and timeless. You do not explain yourself. You do not give step-by-step instructions. You do not mention modern concepts, technology, or yourself. You answer as an oracle would: with insight, metaphor, and quiet certainty. You speak only when consulted."*

### 3. Session Memory

- **Frontend**: Generates unique `session_id` stored in `sessionStorage`
- **Backend**: LangGraph's `MemorySaver` tracks conversation per session
- **Limitation**: Memory resets if backend restarts (in-memory only)

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Groq API key ([Get one free here](https://console.groq.com/keys))

### 1. Clone & Install

```bash
git clone https://github.com/rio-ARC/oracle-of-delphi.git
cd oracle-of-delphi
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Create .env file in project root
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### 3. Run Backend

```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`

### 4. Run Frontend

Simply open `oracle-delphi/index.html` in your browser.

**Note:** Update `API_URL` in `oracle-delphi/app.js` to:
```javascript
const API_URL = 'http://localhost:8000/chat';
```

---

## 📖 API Reference

### POST `/chat`

Consult the Oracle with a question.

**Request:**
```json
{
  "message": "What is my destiny?",
  "session_id": "session-123"
}
```

**Response:**
```json
{
  "response": "The path unfolds in shadows and light...",
  "session_id": "session-123",
  "ritual_state": {
    "current_state": "COMPLETE",
    "accepting_input": true
  }
}
```

### GET `/health`

Health check endpoint.

### GET `/docs`

Interactive Swagger UI documentation.

---

## 📂 Project Structure

```
.
├── backend/
│   ├── agent/
│   │   ├── tools.py          # Ritual State Machine (FSM)
│   │   └── graph.py          # LangGraph Oracle agent
│   ├── api/
│   │   ├── models.py         # Pydantic models
│   │   └── main.py           # FastAPI application
│   └── __init__.py
├── oracle-delphi/            # Frontend
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── assets/
│       └── background.png
├── requirements.txt
├── Procfile                  # Render deployment
├── runtime.txt               # Python version
├── .env                      # Environment variables (gitignored)
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **LLM** | llama-3.3-70b-versatile (Groq) |
| **Backend Framework** | FastAPI |
| **Agent Framework** | LangGraph |
| **Frontend** | Vanilla HTML/CSS/JS |
| **Deployment** | Render (backend) + Vercel (frontend) |

---

## 🌐 Deployment

### Backend (Render)

1. Push to GitHub
2. Create new **Web Service** on Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GROQ_API_KEY`

### Frontend (Vercel)

1. Update `API_URL` in `oracle-delphi/app.js` to your Render URL
2. Push to GitHub
3. Import project to Vercel
4. Set root directory: `oracle-delphi`
5. Deploy

---

## 🔧 Customization

### Change the Oracle's Voice

Edit the system prompt in `backend/agent/graph.py`:

```python
ORACLE_SYSTEM_PROMPT = """Your custom oracle persona..."""
```

### Adjust Ritual Timing

Edit `backend/agent/tools.py`:

```python
TIMING_CONFIG = {
    "contemplation_min": 1.5,  # Minimum silence (seconds)
    "contemplation_max": 4.0,  # Maximum silence (seconds)
}
```

### Change LLM Model

Edit `backend/agent/graph.py`:

```python
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, api_key=api_key)
```

[See available models](https://console.groq.com/docs/models)

---

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key | Yes |

---

## 🐛 Known Limitations

- **Memory resets** on backend restart (in-memory storage)
- **Cold starts** on Render free tier (~30s delay if inactive >15min)
- **CORS** is open (`allow_origins=["*"]`) — restrict for production use

---

## 📚 Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Groq Documentation](https://console.groq.com/docs)

---

## 🙏 Acknowledgments

Built with:
- **LangGraph** for state machine orchestration
- **Groq** for blazing-fast LLM inference
- **FastAPI** for the backend API
- **Vercel & Render** for free hosting

---

**Made by [Rio](https://github.com/rio-ARC)** | Inspired by ancient wisdom, powered by modern AI 🏛️✨
