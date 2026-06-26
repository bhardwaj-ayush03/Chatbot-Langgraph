# 🤖 Chatbot-Langgraph

A production-style, multi-feature conversational AI chatbot built with **LangGraph** and **Streamlit**, supporting persistent memory, real-time streaming, tool calling, and PDF-based RAG — all powered by **Groq** (LLaMA 3.3 70B) and local **Ollama** embeddings.

---

## ✨ Features

| Feature | File(s) |
|---|---|
| Basic stateful chatbot | `chatbot_backend.py` · `chatbot_frontend.py` |
| Persistent conversation history (SQLite) | `chatbot_backend_db.py` · `chatbot_frontend_db.py` |
| Real-time token streaming | `streaming_frontend.py` |
| Multi-thread session management | `threading_frontend.py` |
| Agentic tool calling (search, calculator, stocks) | `chatbot_rag_backend.py` |
| PDF-based RAG (per-thread FAISS retrieval) | `chatbot_rag_backend.py` · `chatbot_rag_frontend.py` |

---

## 🏗️ Architecture

```
User (Streamlit UI)
       │
       ▼
  Streamlit Frontend
       │  HumanMessage
       ▼
  LangGraph StateGraph
  ┌────────────────────────────────┐
  │  START → chat_node             │
  │             │                  │
  │    tools_condition             │
  │         ╱        ╲            │
  │   tool_node    END (direct)   │
  │      │                        │
  │   chat_node ←─────────────── │
  └────────────────────────────────┘
       │  AIMessage (streamed)
       ▼
  Streamlit (st.write_stream)
       │
  SQLite Checkpointer  ←── thread_id scoped memory
```

### RAG Pipeline

```
PDF Upload (Streamlit)
       │
  PyPDFLoader → RecursiveCharacterTextSplitter
       │           chunk_size=1000, overlap=200
       ▼
  OllamaEmbeddings (nomic-embed-text)
       │
  FAISS VectorStore → Retriever (top-k=4)
       │
  Stored in _THREAD_RETRIEVERS[thread_id]
       │
  rag_tool called by LLM at inference time
```

---

## 🧰 Tech Stack

| Layer | Tool | Version |
|---|---|---|
| **LLM** | Groq — `llama-3.3-70b-versatile` | via `langchain-groq` |
| **Embeddings** | Ollama — `nomic-embed-text:latest` | local |
| **Agent Framework** | LangGraph | `>=0.2` |
| **LLM Abstraction** | LangChain Core | `>=0.1` |
| **Vector Store** | FAISS | `faiss-cpu` |
| **Document Loader** | LangChain Community — PyPDFLoader | — |
| **Text Splitter** | RecursiveCharacterTextSplitter | — |
| **Web Search** | DuckDuckGo Search (`ddgs`) | `pip install -U ddgs` |
| **Stock Price** | Alpha Vantage REST API | free tier |
| **Persistence** | SQLite + `langgraph-checkpoint-sqlite` | — |
| **Frontend** | Streamlit | `>=1.30` |
| **Env Management** | python-dotenv | — |
| **Language** | Python | `3.10+` |

---

## 📁 Project Structure

```
Chatbot-Langgraph/
│
├── chatbot_backend.py              # Basic LangGraph chatbot (in-memory)
├── chatbot_frontend.py             # Streamlit UI for basic chatbot
│
├── chatbot_backend_db.py           # Chatbot with SQLite persistence
├── chatbot_frontend_db.py          # Streamlit UI with thread history
│
├── streaming_frontend.py           # Token-level streaming via st.write_stream
├── threading_frontend.py           # Multi-session thread management
│
├── chatbot_rag_backend.py          # Full agentic backend: tools + RAG
├── chatbot_rag_frontend.py         # Full Streamlit UI with PDF upload
│
├── requirements.txt
├── .gitignore
└── .env                            # (not committed) — API keys
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/bhardwaj-ayush03/Chatbot-Langgraph.git
cd Chatbot-Langgraph
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -U ddgs              # required by DuckDuckGoSearchRun
```

### 4. Pull the embedding model via Ollama

```bash
# Install Ollama: https://ollama.com
ollama pull nomic-embed-text
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free Groq API key at [console.groq.com](https://console.groq.com)

---

## 🚀 Running the App

### Full RAG Chatbot (recommended)

```bash
streamlit run chatbot_rag_frontend.py
```

### Other entry points

```bash
streamlit run chatbot_frontend.py         # basic chatbot
streamlit run chatbot_frontend_db.py      # with SQLite persistence
streamlit run streaming_frontend.py       # streaming demo
streamlit run threading_frontend.py       # multi-thread demo
```

---

## 🛠️ Available Tools (Agentic Mode)

| Tool | Description |
|---|---|
| `DuckDuckGoSearchRun` | Live web search via DuckDuckGo |
| `get_stock_price` | Fetches real-time stock data from Alpha Vantage |
| `calculator` | Arithmetic — add, sub, mul, div |
| `rag_tool` | Retrieves relevant chunks from the uploaded PDF for the active thread |

---

## 💾 Persistence

Conversation history is stored in a local **SQLite** database (`chatbot.db`) using LangGraph's `SqliteSaver` checkpointer, scoped by `thread_id`. Each conversation thread maintains its own independent message history and document retriever.

---

## 🔑 Key Design Decisions

- **Thread-scoped RAG:** Each Streamlit session gets its own `thread_id`. Uploaded PDFs are indexed into a FAISS store keyed by `thread_id`, so document context never leaks across conversations.
- **Streaming:** The frontend uses `stream_mode="messages"` with `st.write_stream` to yield tokens as they arrive from Groq.
- **Tool safety:** `tools_condition` from LangGraph's prebuilt module handles the LLM → tool → LLM loop cleanly without manual routing logic.

---

## 📦 requirements.txt (key packages)

```
langchain
langchain-core
langchain-groq
langchain-ollama
langchain-community
langchain-text-splitters
langgraph
langgraph-checkpoint-sqlite
faiss-cpu
pypdf
streamlit
python-dotenv
requests
ddgs
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 👤 Author

**Ayush Bhardwaj**


[![GitHub](https://img.shields.io/badge/GitHub-bhardwaj--ayush03-181717?logo=github)](https://github.com/bhardwaj-ayush03)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-ayushbhardwaj03-0A66C2?logo=linkedin)](https://linkedin.com/in/ayushbhardwaj03)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
