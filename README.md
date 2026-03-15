# Cortex Research Assistant

A Streamlit app that runs a 4‑stage research pipeline (Planner → Researcher → Writer → Reviewer) to generate structured reports on any topic.

## Deployed App

- Streamlit: https://cortex-research-assistant-9y35zk3ygx4agiaurrcnx5.streamlit.app/

## Features

- Multi‑agent pipeline: plan, web research, draft, review
- DuckDuckGo web search via `ddgs`
- Groq LLM backend (default model: `llama-3.3-70b-versatile`)
- Streamlit UI with tone + report style controls
- Saves reports to `outputs/` (local/dev)

## Tech Stack

- Python + Streamlit
- Groq SDK
- DuckDuckGo search (`ddgs`)
- Optional: ChromaDB vector store (`src/vector_store.py`)

## Project Structure

- `app.py` — Streamlit UI
- `src/agents.py` — agent prompts + Groq call wrapper
- `src/tools.py` — web search helpers
- `src/main.py` — CLI-style orchestrator + report saving
- `src/vector_store.py` — optional document ingestion + retrieval (ChromaDB)

## Local Setup

### 1) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Configure secrets

You need a Groq API key.

Option A — local `.env` (development):

Create a `.env` file in the project root:

```env
GROQ_API_KEY="YOUR_KEY"
```

Option B — environment variable:

```powershell
$env:GROQ_API_KEY="YOUR_KEY"
```

### 4) Run the app

```powershell
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push the repo to GitHub.
2. On https://share.streamlit.io click **New app**.
3. Select this repo and set the main file to `app.py`.
4. In **App settings → Secrets**, add:

```toml
GROQ_API_KEY = "YOUR_KEY"
```

## Notes

- `outputs/` and `vector_db/` are generated locally and are ignored by Git.
- Streamlit Cloud storage is ephemeral: files written at runtime may not persist across restarts.

## Troubleshooting

- **Missing `GROQ_API_KEY`**: add it via Streamlit Secrets or your environment.
- **Slow installs**: `chromadb` and `sentence-transformers` can take time due to large wheels.

## License

Add a license if you plan to distribute this publicly.
