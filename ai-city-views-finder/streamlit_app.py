"""
City Views Finder - Streamlit Frontend
========================================

Streamlit application that provides a user-friendly interface for the City Views Finder agent.
Includes Cloud Run monitoring integration.

Author: Adri
Date: 2026-01-11
"""

import streamlit as st
import asyncio
import os
import vertexai
from vertexai import agent_engines
from pathlib import Path
import logging
from datetime import datetime
from google.cloud import logging as cloud_logging
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID = os.getenv("PROJECT_ID", "gen-lang-client-0495395701")
LOCATION = os.getenv("LOCATION", "us-central1")

# Read agent resource name from file or environment
AGENT_RESOURCE_NAME = os.getenv("AGENT_RESOURCE_NAME", "")
if not AGENT_RESOURCE_NAME:
    resource_file = Path("agent_resource_name.txt")
    if resource_file.exists():
        AGENT_RESOURCE_NAME = resource_file.read_text().strip()

# ============================================================================
# LOGGING & MONITORING SETUP
# ============================================================================

# Setup Cloud Logging for monitoring
def setup_cloud_logging():
    """Setup Cloud Logging client for monitoring in Cloud Run"""
    try:
        client = cloud_logging.Client(project=PROJECT_ID)
        client.setup_logging()
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        return logger
    except Exception as e:
        # Fallback to standard logging if Cloud Logging is not available
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.warning(f"Cloud Logging not available: {e}")
        return logger

logger = setup_cloud_logging()

# ============================================================================
# MONITORING FUNCTIONS
# ============================================================================

def log_user_interaction(user_id: str, message: str, response_time: float = None):
    """Log user interactions for monitoring"""
    log_data = {
        "event": "user_query",
        "user_id": user_id,
        "message_length": len(message),
        "timestamp": datetime.utcnow().isoformat(),
        "project_id": PROJECT_ID,
    }

    if response_time:
        log_data["response_time_seconds"] = response_time

    logger.info(json.dumps(log_data))

def log_agent_response(user_id: str, session_id: str, message: str, response_length: int, response_time: float):
    """Log agent responses for monitoring"""
    log_data = {
        "event": "agent_response",
        "user_id": user_id,
        "session_id": session_id,
        "query_length": len(message),
        "response_length": response_length,
        "response_time_seconds": response_time,
        "timestamp": datetime.utcnow().isoformat(),
        "project_id": PROJECT_ID,
    }

    logger.info(json.dumps(log_data))

def log_error(error_type: str, error_message: str, user_id: str = None):
    """Log errors for monitoring"""
    log_data = {
        "event": "error",
        "error_type": error_type,
        "error_message": error_message,
        "timestamp": datetime.utcnow().isoformat(),
        "project_id": PROJECT_ID,
    }

    if user_id:
        log_data["user_id"] = user_id

    logger.error(json.dumps(log_data))

# ============================================================================
# STREAMLIT UI CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="City Views Finder",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .agent-message {
        background-color: #f5f5f5;
    }
    .info-box {
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        background-color: #f0f8ff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "user_id" not in st.session_state:
    # Generate a unique user ID for this session
    st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

if "remote_app" not in st.session_state:
    st.session_state.remote_app = None

# ============================================================================
# AGENT INITIALIZATION
# ============================================================================

@st.cache_resource
def initialize_agent():
    """Initialize the agent connection (cached)"""
    try:
        logger.info(f"Initializing Vertex AI with project: {PROJECT_ID}, location: {LOCATION}")
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        logger.info(f"Getting agent: {AGENT_RESOURCE_NAME}")
        remote_app = agent_engines.get(AGENT_RESOURCE_NAME)

        logger.info("Agent initialized successfully")
        return remote_app
    except Exception as e:
        error_msg = f"Error initializing agent: {e}"
        log_error("agent_initialization", str(e))
        logger.error(error_msg)
        return None

# ============================================================================
# AGENT INTERACTION FUNCTIONS
# ============================================================================

async def create_session(remote_app, user_id: str):
    """Create a new session for the user"""
    try:
        logger.info(f"Creating session for user: {user_id}")
        session = await remote_app.async_create_session(user_id=user_id)
        session_id = session["id"]
        logger.info(f"Session created: {session_id}")
        return session_id
    except Exception as e:
        error_msg = f"Error creating session: {e}"
        log_error("session_creation", str(e), user_id)
        logger.error(error_msg)
        raise

async def query_agent(remote_app, user_id: str, session_id: str, message: str):
    """Query the agent and stream the response"""
    start_time = datetime.now()
    response_text = ""

    try:
        log_user_interaction(user_id, message)

        async for event in remote_app.async_stream_query(
            user_id=user_id,
            session_id=session_id,
            message=message,
        ):
            # Handle dictionary events (from Agent Engine)
            if isinstance(event, dict):
                # Extract text from event['content']['parts'][0]['text']
                if 'content' in event:
                    content = event['content']
                    if 'parts' in content and isinstance(content['parts'], list):
                        for part in content['parts']:
                            if 'text' in part and part['text']:
                                text = part['text']
                                response_text += text
                                yield text
            # Handle object events (fallback for other event types)
            elif hasattr(event, 'text') and event.text:
                text = event.text
                response_text += text
                yield text
            elif hasattr(event, 'content'):
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            text = part.text
                            response_text += text
                            yield text
                elif hasattr(event.content, 'text') and event.content.text:
                    text = event.content.text
                    response_text += text
                    yield text

        # Log the complete response
        response_time = (datetime.now() - start_time).total_seconds()
        log_agent_response(user_id, session_id, message, len(response_text), response_time)

    except Exception as e:
        error_msg = f"Error querying agent: {e}"
        log_error("agent_query", str(e), user_id)
        logger.error(error_msg)
        raise

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">🏔️ City Views Finder</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Discover the best viewpoints, routes, and natural enclaves around any city</p>',
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This AI agent helps you discover:
        - 🌄 Scenic viewpoints and lookouts
        - 🛣️ Panoramic routes and drives
        - 🏨 Paradores with exceptional views
        - 🌲 Beautiful natural enclaves

        Simply enter a city name and let the agent find the most stunning spots!
        """)

        st.divider()

        # System Status
        st.header("📊 System Status")

        if st.session_state.remote_app:
            st.success("✅ Agent Connected")
        else:
            st.warning("⏳ Connecting to agent...")

        if st.session_state.session_id:
            st.info(f"Session: {st.session_state.session_id[:8]}...")

        st.caption(f"User ID: {st.session_state.user_id}")

        st.divider()

        # Clear conversation button
        if st.button("🔄 New Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = None
            logger.info(f"Conversation reset for user: {st.session_state.user_id}")
            st.rerun()

    # Initialize agent if not already done
    if st.session_state.remote_app is None:
        with st.spinner("Connecting to agent..."):
            st.session_state.remote_app = initialize_agent()

        if st.session_state.remote_app is None:
            st.error("❌ Failed to connect to the agent. Please check the configuration.")
            st.code(f"Project: {PROJECT_ID}\nLocation: {LOCATION}\nAgent: {AGENT_RESOURCE_NAME}")
            return

    # Create session if not exists
    if st.session_state.session_id is None:
        try:
            import nest_asyncio
            nest_asyncio.apply()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            st.session_state.session_id = loop.run_until_complete(
                create_session(st.session_state.remote_app, st.session_state.user_id)
            )
        except Exception as e:
            st.error(f"❌ Failed to create session: {e}")
            logger.error(f"Session creation error: {e}")
            return

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Enter a city name (e.g., 'Find the best viewpoints around Málaga')"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # Collect response using event loop
                import nest_asyncio
                nest_asyncio.apply()

                async def collect_response():
                    response = ""
                    async for chunk in query_agent(
                        st.session_state.remote_app,
                        st.session_state.user_id,
                        st.session_state.session_id,
                        prompt
                    ):
                        response += chunk
                        # Update display in real-time
                        message_placeholder.markdown(response + "▌")
                    return response

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                full_response = loop.run_until_complete(collect_response())
                message_placeholder.markdown(full_response)

            except Exception as e:
                error_msg = f"❌ Error: {e}"
                message_placeholder.error(error_msg)
                full_response = error_msg

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
