"""
FastAPI Entry Point for Cloud Run Deployment

This module creates the FastAPI application that serves the ADK agent
and optionally the web interface.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize tracing before importing ADK components
from observability.tracing import setup_tracing

setup_tracing()

from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

# Configuration
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost,http://localhost:8080,http://localhost:8501,*",
).split(",")
SERVE_WEB_INTERFACE = os.getenv("SERVE_WEB_INTERFACE", "true").lower() == "true"

# Create app using ADK's FastAPI helper
app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)


# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy", "service": "videogames-assistant"}


@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        "service": "AI Video Games Assistant",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
