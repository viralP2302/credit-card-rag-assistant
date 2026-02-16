# Finance RAG API

A FastAPI-based **Retrieval-Augmented Generation (RAG)** API for credit card Q&A, built with LangGraph and LangChain. It uses a credit card dataset to build a knowledge base and answers user questions about cards, rewards, and eligibility.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.99+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-orange.svg)

---

## Demo

**Add a short screen recording (GIF or video)** for showcase: run the API, open `/docs`, try a query like **"Which card has the best cashback for groceries?"** and show the response. Save the recording as **`.github/images/demo.gif`**; then the image below will display.

<!-- Once you add .github/images/demo.gif, the next line will show it -->
![Demo](.github/images/demo.gif)

*Use a query different from the upstream template (e.g. not "What's the best card for travel?"). Good options:* **"Which card has the best cashback for groceries?"** or **"Recommend a card with no annual fee and a good sign-up bonus"**.

---

## Features

- **RAG pipeline**: Embeddings + vector store (in-memory) + LLM for grounded answers
- **Credit card QA**: Pre-loaded knowledge base from structured card data
- **LangGraph agent**: Query → retrieve → generate flow
- **FastAPI**: OpenAPI docs at `/docs`, health check at `/health`
- **Python 3.9+**: Modern async API

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) – API framework
- [LangChain](https://www.langchain.com) / [LangGraph](https://www.langchain.com/langgraph) – RAG and agent graph
- [HuggingFace sentence-transformers](https://huggingface.co/sentence-transformers) – embeddings
- OpenAI (e.g. `gpt-4o-mini`) – chat model

---

## Get started

### Prerequisites

- **Python 3.9+** – check with `python3 --version`
- **OpenAI API key** – [create one here](https://platform.openai.com/api-keys)

### Clone and setup

```bash
git clone https://github.com/YOUR_USERNAME/finance-rag-api.git
cd finance-rag-api
```

### Virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# or: venv\Scripts\activate.bat   # Windows
```

### Dependencies

```bash
pip install -r requirements.txt
```

### Run locally

From the **project root**:

```bash
export OPENAI_API_KEY=your_api_key_here
uvicorn app.main:app --reload
```

API base: **http://localhost:8000**

- **Docs (Swagger):** http://localhost:8000/docs  
- **Health:** http://localhost:8000/health  
- **Ask the bot:** `GET /askBot?query=...&user_name=...`

Try a query different from the upstream demo, e.g. **"Which card has the best cashback for groceries?"** or **"Recommend a card with no annual fee."**

---

## Code structure

| Path | Description |
|------|-------------|
| `app/main.py` | FastAPI app, `/health`, `/askBot` |
| `app/rag/agent.py` | LangGraph RAG agent, vector store, embeddings |
| `app/models/graph_state.py` | Shared state for the graph |
| `app/rag/credit_cards.json` | Credit card knowledge base (from ETL) |
| `etl/` | Optional ETL: Excel → JSON for the dataset |

---

## API overview

- **`GET /health`** – Returns `{"status": "ok", "service": "finance-rag-api"}`.
- **`GET /askBot`** – Query params: `query` (string), `user_name` (string). Returns the model’s answer as plain text.

---

## Resources

- [LangChain tutorials](https://python.langchain.com/docs/tutorials/)
- [LangGraph intro](https://academy.langchain.com/courses/intro-to-langgraph)
- [RAG with LangChain](https://python.langchain.com/docs/tutorials/rag/)
- [FastAPI docs](https://fastapi.tiangolo.com/)

---

## Publish to your GitHub

This repo has **no upstream git history** (clean single-branch history). To push to your GitHub:

1. Create a **new empty repo** on GitHub (e.g. `finance-rag-api` or `credit-card-rag-assistant`).
2. Add it as `origin` and push:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

---

## Attribution

This project is based on [paranjapeved/fastapi-rag-template](https://github.com/paranjapeved/fastapi-rag-template). Extended with a health endpoint, updated dependencies, and this README.
