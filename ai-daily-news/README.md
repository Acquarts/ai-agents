# AI Daily News

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Anthropic](https://img.shields.io/badge/Claude-Haiku_4.5-D4A574?logo=anthropic&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-FF4B4B?logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/github/license/Acquarts/ai-agents)

Real-time AI news curator. Fetches articles from multiple RSS sources and uses Claude to select and summarize the 15 most relevant stories of the day.

DEMO LIVE: https://ai-news-agent-01.streamlit.app/

## How it works

1. User opens the dashboard
2. The agent fetches articles from 9 RSS sources in parallel (~3s)
3. Claude selects the 15 most relevant and summarizes them in a single call (~10s)
4. Results are cached in SQLite — subsequent visits are instant
5. A "Refresh" button lets users force a new fetch

## Architecture

```
agents/
  sources.py          # RSS sources (HuggingFace, ArXiv, OpenAI, Google AI, etc.)
  news_fetcher.py     # Concurrent RSS feed fetching (6 parallel workers)
  summarizer.py       # Selection + summarization via Claude (single call)
  storage_agent.py    # SQLite cache
  orchestrator.py     # Orchestrates fetch → curate → cache
  run_pipeline.py     # CLI entry point

streamlit_app.py      # Web dashboard
db/news.db            # SQLite cache (created automatically)
```

## Sources

| Source | Category |
|--------|----------|
| ArXiv CS.AI | Research |
| HuggingFace Blog | Research |
| Google AI Blog | Research |
| DeepMind Blog | Research |
| MIT Technology Review | Industry |
| VentureBeat AI | Industry |
| The Verge AI | Products |
| OpenAI Blog | Products |
| Towards Data Science | Tooling |

## Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

### Dashboard

```bash
streamlit run streamlit_app.py
```

### CLI

```bash
python agents/run_pipeline.py
```

## Deploy to Streamlit Cloud

1. Push the repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect the repo and select `ai-daily-news/streamlit_app.py`
4. Add `ANTHROPIC_API_KEY` in Settings → Secrets

## Stack

- **Claude Haiku 4.5** — article curation and summarization
- **Streamlit** — web dashboard
- **SQLite** — daily cache
- **feedparser** — RSS parsing
- **Anthropic SDK** — Claude API client
