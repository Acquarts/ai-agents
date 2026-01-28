# AI Video Games Assistant

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Google ADK](https://img.shields.io/badge/Google_ADK-1.2+-4285F4?logo=google&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-8E75B2?logo=googlegemini&logoColor=white)
![Vertex AI](https://img.shields.io/badge/Vertex_AI-4285F4?logo=googlecloud&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-4285F4?logo=googlecloud&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)
![Arize AX](https://img.shields.io/badge/Arize_AX-Observability-FF6F00)
![YouTube API](https://img.shields.io/badge/YouTube_Data_API-v3-FF0000?logo=youtube&logoColor=white)

An AI-powered video game assistant built with **Google Agent Development Kit (ADK)** and **Gemini 2.5 Flash**. Features a multi-agent architecture with specialized sub-agents for YouTube video search, web search, and URL verification.

## Architecture

```
┌─────────────────────────────────────────────┐
│              Videogames_Assistant            │
│              (Root Agent)                    │
│                                             │
│  Tools:                                     │
│  ├── GoogleSearchTool (web search)          │
│  └── UrlContextTool (URL verification)      │
│                                             │
│  Sub-agents:                                │
│  └── youtube_searching                      │
│      └── search_youtube (YouTube Data API)  │
└─────────────────────────────────────────────┘
```

### Capabilities

- **Game Recommendations** — Personalized suggestions based on preferences, platform, and genre
- **Technical Analysis** — Graphics, performance, optimization comparisons
- **YouTube Search** — Direct video search via YouTube Data API v3 with real URLs
- **Web Search** — Up-to-date information on releases, news, prices
- **Troubleshooting** — Performance issues, configurations, system requirements

## Project Structure

```
ai-videogames-assistant/
├── .github/workflows/
│   ├── ci.yml                # Lint, type check, tests
│   └── deploy.yml            # Build & deploy to Cloud Run
├── my_agent/
│   ├── __init__.py           # Package exports + tracing init
│   ├── agent.py              # Agent definitions
│   └── youtube_tool.py       # YouTube Data API integration
├── app/
│   ├── adk_service.py        # ADK session management (singleton)
│   └── streamlit_app.py      # Streamlit chat UI
├── observability/
│   └── tracing.py            # Arize AX instrumentation
├── tests/
│   └── test_agent.py         # Agent structure tests
├── main.py                   # FastAPI entry point (Cloud Run)
├── Dockerfile                # Container configuration
├── requirements.txt          # Production dependencies
└── requirements-dev.txt      # Development dependencies
```

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud project with billing enabled
- YouTube Data API v3 enabled
- Arize AX account (for observability)

### Local Setup

```bash
# Clone and setup
git clone https://github.com/<your-org>/ai-videogames-assistant.git
cd ai-videogames-assistant

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Run Locally

```bash
# Option 1: ADK built-in UI
adk web my_agent

# Option 2: Streamlit UI
streamlit run app/streamlit_app.py

# Option 3: FastAPI server
uvicorn main:app --reload --port 8080
```

### Run with Docker

```bash
docker build -t videogames-assistant .
docker run -p 8080:8080 --env-file .env videogames-assistant
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_CLOUD_PROJECT` | GCP project ID | Yes |
| `GOOGLE_CLOUD_LOCATION` | GCP region (default: `us-central1`) | Yes |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI (`True`/`False`) | Yes |
| `YOUTUBE_API_KEY` | YouTube Data API v3 key | Yes |
| `ARIZE_SPACE_ID` | Arize AX space ID | For tracing |
| `ARIZE_API_KEY` | Arize AX API key | For tracing |
| `ARIZE_PROJECT_NAME` | Arize project name | For tracing |

## Deployment

### Cloud Run (via CI/CD)

Push to `main` triggers automatic deployment via GitHub Actions:

1. **CI** (`ci.yml`) — Runs lint, type check, and tests
2. **Deploy** (`deploy.yml`) — Builds Docker image, pushes to Artifact Registry, deploys to Cloud Run

#### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `GCP_PROJECT_ID` | Google Cloud project ID |
| `WIF_PROVIDER` | Workload Identity Federation provider |
| `WIF_SERVICE_ACCOUNT` | Service account email |

#### GCP Setup (one-time)

```bash
# Enable APIs
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    iamcredentials.googleapis.com \
    youtube.googleapis.com

# Create Artifact Registry
gcloud artifacts repositories create videogames-assistant-repo \
    --repository-format=docker \
    --location=us-central1
```

### Vertex AI Agent Engine

```bash
adk deploy agent_engine \
    --project=$PROJECT_ID \
    --region=us-central1 \
    --staging_bucket=gs://${PROJECT_ID}-agent-engine \
    ./my_agent
```

## Observability

Tracing is handled via **Arize AX** with OpenTelemetry instrumentation:

- LLM call latency and token usage
- Agent routing and sub-agent invocations
- Tool execution (YouTube API, Google Search)
- Error tracking and retry patterns

Configure `ARIZE_SPACE_ID` and `ARIZE_API_KEY` in your environment to enable tracing.

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | Google ADK |
| LLM | Gemini 2.5 Flash |
| Web UI | Streamlit |
| API Server | FastAPI + Uvicorn |
| Observability | Arize AX + OpenTelemetry |
| Container | Docker |
| Cloud Platform | Google Cloud (Vertex AI, Cloud Run) |
| CI/CD | GitHub Actions |
| Video Search | YouTube Data API v3 |
