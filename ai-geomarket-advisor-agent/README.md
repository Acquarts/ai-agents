# GeoMarket Advisor

AI-powered business location analysis using Google Maps and Gemini AI to help entrepreneurs find the best locations for their businesses.

## Overview

GeoMarket Advisor is an intelligent agent that analyzes cities using Google Maps data to identify optimal locations for establishing specific types of businesses. It evaluates factors such as competition density, customer flow potential, nearby points of interest, and overall commercial suitability.

## Architecture

The project consists of two main services:

- **Backend Runtime** ([geomarket_advisor_runtime](geomarket_advisor_runtime/)): FastAPI server with Google ADK agent integration
- **Frontend UI** ([geomarket_advisor_ui](geomarket_advisor_ui/)): Streamlit web interface for user interaction

## Features

- Strategic business location analysis
- Competition density assessment
- Data-driven zone recommendations
- Integration with Google Maps via Model Context Protocol (MCP)
- Real-time analysis through conversational AI
- Clean, intuitive web interface

## Prerequisites

- Docker and Docker Compose
- Google API Key (for Gemini)
- Google Maps API Key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-geomarket-advisor-agent
```

2. Configure environment variables:

Create or edit [geomarket_advisor_runtime/.env](geomarket_advisor_runtime/.env):
```env
GOOGLE_API_KEY=your_google_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Usage

1. Access the web interface at `http://localhost:8501`

2. Enter your business details:
   - **Business type**: e.g., Bakery, Coffee shop, Gym
   - **City**: e.g., Málaga, Madrid, Barcelona

3. Click "Analyze" to receive:
   - Summary of findings
   - 2-3 recommended zones within the city
   - Competition level assessment for each zone
   - Data-driven justification for recommendations

## API Endpoints

### POST `/run`

Run the GeoMarket Advisor agent with a business query.

**Request:**
```json
{
  "query": "Bakery in Málaga",
  "user_id": "optional-user-id",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Analysis results..."
}
```

## Technology Stack

### Backend
- **Google ADK** (Agent Development Kit)
- **Gemini 2.5 Flash** (LLM)
- **FastAPI** (Web framework)
- **MCP** (Model Context Protocol)
- **Google Maps API**

### Frontend
- **Streamlit** (UI framework)
- **Python Requests**

## Project Structure

```
ai-geomarket-advisor-agent/
├── docker-compose.yml
├── geomarket_advisor_runtime/
│   ├── agent.py           # Agent configuration and instructions
│   ├── server.py          # FastAPI server
│   ├── config.py          # Configuration settings
│   ├── tools.py           # Agent tools
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env              # Environment variables
└── geomarket_advisor_ui/
    ├── app.py            # Streamlit application
    ├── Dockerfile
    └── requirements.txt
```

## Services

### Backend Runtime
- **Port**: 8000
- **Container**: geomarket_advisor_runtime
- **Endpoints**: `/run`

### Frontend UI
- **Port**: 8501
- **Container**: geomarket_advisor_ui
- **Access**: http://localhost:8501

## Development

### Run Backend Locally
```bash
cd geomarket_advisor_runtime
pip install -r requirements.txt
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Run Frontend Locally
```bash
cd geomarket_advisor_ui
pip install -r requirements.txt
streamlit run app.py
```

## License

This project is private. All rights reserved.

## Notes

- The agent uses only real data from Google Maps MCP
- No fabricated metrics or unsupported assumptions are made
- All recommendations are based on observable patterns from map data
- Requires active Google API credentials with appropriate quotas

