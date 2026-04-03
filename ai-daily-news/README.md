# AI Daily News

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Anthropic](https://img.shields.io/badge/Claude-Haiku_4.5-D4A574?logo=anthropic&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/github/license/Acquarts/ai-agents)

Automated AI news pipeline. Collects articles from multiple RSS sources, summarizes them with Claude (Haiku), and displays them in a Streamlit dashboard.

## Architecture

```
agents/
  sources.py          # RSS sources (HuggingFace, ArXiv, OpenAI, Google AI, etc.)
  news_fetcher.py     # Concurrent RSS feed fetching
  summarizer.py       # Summaries via Claude API (Haiku 4.5)
  storage_agent.py    # SQLite persistence
  orchestrator.py     # Orchestrates the full pipeline
  run_pipeline.py     # Pipeline entry point

scheduler/
  register_task.py    # Scheduled task (Windows Task Scheduler)

streamlit_app.py      # Web dashboard
db/news.db            # SQLite database (created automatically)
```

## Requirements

- Python 3.12+
- Anthropic API key

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

### Run the pipeline

```bash
python agents/run_pipeline.py
```

This will:
1. Fetch articles from 9 RSS sources (HuggingFace, ArXiv, MIT Tech Review, VentureBeat, The Verge, OpenAI, Google AI, DeepMind, Towards Data Science)
2. Save new articles to SQLite
3. Summarize unsummarized articles with Claude Haiku
4. Classify by category (Research, Products, Industry, Tooling) and importance (high, medium, low)

### View the dashboard

```bash
streamlit run streamlit_app.py
```

### Schedule daily execution (Windows)

```bash
python scheduler/register_task.py
```

Registers a Windows Task Scheduler job that runs the pipeline every day at 7:00 AM.

## Deploy to Streamlit Cloud

1. Push the repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo and select `streamlit_app.py`
4. Set the `ANTHROPIC_API_KEY` secret in the app settings

> **Note:** Streamlit Cloud uses ephemeral storage. For production, consider using an external database (PostgreSQL, Supabase, etc.) instead of SQLite.

## Stack

- **Claude Haiku 4.5** — article summarization and classification
- **Streamlit** — web dashboard
- **SQLite** — local storage
- **feedparser** — RSS parsing
- **Anthropic SDK** — Claude API client
