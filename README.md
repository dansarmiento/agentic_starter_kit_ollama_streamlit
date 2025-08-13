# Agentic AI Starter (Python + Ollama) — with Streamlit UI

A beginner-friendly, production-lean starter for building agentic AI patterns locally using Python and Ollama.
Includes Self-Check, ReAct, Planner–Executor, Reflection, and RAG. Now with a Streamlit app.

## Features
- Minimal Ollama client (HTTP) with streaming support
- Patterns: Self-Check, ReAct (with tools), Planner–Executor, Reflection, RAG (ChromaDB + SentenceTransformers)
- Streamlit UI with tabs for each pattern
- Makefile targets, mocked tests that don’t require a running LLM

---

## Install Ollama

### macOS / Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
# (Linux) ensure service
sudo systemctl enable ollama
sudo systemctl start ollama
```

### Windows
Download and run the official installer from https://ollama.com. The service starts automatically.

### Sanity check
```bash
ollama list
ollama pull llama3.1:8b-instruct
ollama run llama3.1:8b-instruct "Say 'ready'."
```
The local API is at `http://127.0.0.1:11434`.

---

## Project Setup
```bash
# Clone or create the folder
mkdir agentic-ai-starter && cd agentic-ai-starter

# (Recommended) Use a venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Python deps
pip install --upgrade pip
pip install -r requirements.txt

# Pull at least one model
ollama pull llama3.1:8b-instruct
```

### Quick Start (CLI demo)
```bash
make run-demo
```

### Launch Streamlit UI
```bash
make run-ui
# or
streamlit run app.py
```

### Run tests (fast, mocked)
```bash
make test
```

---

## Make Targets
- `make install` — install deps
- `make run-demo` — run the integrated demo
- `make run-ui` — launch the Streamlit app
- `make test` — run unit tests (mocked)
- `make clean` — remove caches and build artifacts

---

## Model Recommendations
- `llama3.1:8b-instruct` — fast and capable generalist
- `qwen2.5:14b-instruct` (or `7b`) — stronger coding/reasoning
- `mixtral:8x7b-instruct` — MoE; solid long-form reasoning

Pull examples:
```bash
ollama pull llama3.1:8b-instruct
ollama pull qwen2.5:14b-instruct
ollama pull mixtral:8x7b-instruct
```

---

## Prompt Templates (dev assist)
See `src/prompts/dev_assist_templates.md` for templates covering: Task→Code, Refactor, Tests, Docs/Types, Design-first, and ReAct tool-use.

---

## Notes
- The RAG pipeline (ChromaDB + `all-MiniLM-L6-v2`) builds a tiny local vector store from files in `data/` on first run.
- `tests/` use a `DummyClient` to validate orchestration without an LLM.
