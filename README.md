# Finance RAG API

A **Retrieval-Augmented Generation (RAG)** API for credit card Q&A—built with **FastAPI**, **LangGraph**, and **LangChain**. Ask questions in natural language and get answers grounded in a structured credit card knowledge base. Runs with **Ollama** (no API key) or OpenAI.

[![Python](https://img.shields.io/badge/Python-3.9+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.99+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-1c3c3c?logo=langchain)](https://www.langchain.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent-1c3c3c)](https://www.langchain.com/langgraph)

---

## What this project does

- **RAG pipeline:** Embed credit card data, retrieve relevant chunks for each query, generate answers with an LLM.
- **Dual LLM support:** Use **Ollama** locally (no API key) or **OpenAI** (set `OPENAI_API_KEY`).
- **Production-style API:** FastAPI with OpenAPI docs, health check, and a single `/askBot` endpoint.
- **Financial domain:** Pre-loaded dataset and prompts tuned for credit card–related questions (rewards, fees, eligibility).

---

## Demo

<video src="demo_video/demo.mov" controls width="700"></video>

*Screen recording: Swagger UI → GET /askBot with a credit card query → model response.*

---

## Tech stack

| Layer        | Technology |
|-------------|------------|
| API         | FastAPI, Uvicorn |
| RAG / Agent | LangChain, LangGraph |
| Embeddings  | HuggingFace `sentence-transformers/all-mpnet-base-v2` |
| Vector store| In-memory (LangChain) |
| LLM         | Ollama (default, e.g. `llama3.2`) or OpenAI `gpt-4o-mini` |

---

## Quick start

**Prerequisites:** Python 3.9+, and either [Ollama](https://ollama.com) (recommended) or an OpenAI API key.

```bash
git clone https://github.com/viralP2302/credit-card-rag-assistant.git
cd credit-card-rag-assistant
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Run with Ollama (no API key):**

```bash
ollama pull llama3.2    # one-time
uvicorn app.main:app --reload
```

**Or with OpenAI:**

```bash
export OPENAI_API_KEY=your_key
uvicorn app.main:app --reload
```

- **API docs:** http://localhost:8000/docs  
- **Health:** http://localhost:8000/health  
- **Ask the bot:** `GET /askBot?query=...&user_name=...`

---

## API

| Endpoint    | Method | Description |
|------------|--------|-------------|
| `/health`  | GET    | Returns `{"status":"ok","service":"finance-rag-api"}`. |
| `/askBot`  | GET    | **query** (string), **user_name** (string). Returns the model’s answer as plain text. |

Use the **Swagger UI** at `/docs` to try both.

---

## Project structure

```
├── app/
│   ├── main.py           # FastAPI app, /health, /askBot
│   ├── rag/
│   │   ├── agent.py      # LangGraph RAG agent, Ollama/OpenAI, vector store
│   │   └── credit_cards.json
│   └── models/
│       └── graph_state.py
├── etl/                  # Optional: Excel → JSON for the dataset
├── requirements.txt
└── README.md
```

---

## Environment (optional)

| Variable         | Description |
|------------------|-------------|
| `OPENAI_API_KEY` | If set, uses OpenAI instead of Ollama. |
| `OLLAMA_MODEL`   | Ollama model name (default: `llama3.2`). |
| `USE_OLLAMA`     | Set to `1` to force Ollama even if `OPENAI_API_KEY` is set. |

---

## Attribution

Based on [paranjapeved/fastapi-rag-template](https://github.com/paranjapeved/fastapi-rag-template). Extended with Ollama support, health endpoint, Pydantic v2, and this README.
