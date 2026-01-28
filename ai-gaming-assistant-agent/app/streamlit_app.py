"""
Streamlit Chat Interface for AI Video Games Assistant

This module provides a chat-based UI for interacting with the
ADK-powered video games assistant agent.
"""

import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import asyncio
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize page config first (must be first Streamlit command)
st.set_page_config(
    page_title="AI Video Games Assistant",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Initialize observability
try:
    from observability.tracing import setup_tracing
    setup_tracing()
except ImportError:
    pass  # Tracing not available

from app.adk_service import get_adk_service


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"

    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"

    if "adk_service" not in st.session_state:
        st.session_state.adk_service = get_adk_service()


def run_async(coro):
    """Helper to run async code in Streamlit's sync context."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def render_sidebar():
    """Render the sidebar with session info and controls."""
    with st.sidebar:
        st.title("🎮 Settings")

        st.markdown("---")
        st.subheader("Session Info")
        st.text(f"User: {st.session_state.user_id[:12]}...")
        st.text(f"Session: {st.session_state.session_id[:12]}...")

        st.markdown("---")

        if st.button("🔄 New Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"
            st.rerun()

        st.markdown("---")
        st.markdown(
            """
        ### About
        This assistant can help you with:
        - 🎯 Game recommendations
        - 📊 Technical analysis
        - 🔧 Troubleshooting
        - 📺 YouTube video search
        - 📰 Gaming news
        """
        )

        st.markdown("---")
        st.caption("Powered by Google ADK & Gemini")


def render_chat_history():
    """Render the chat message history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input():
    """Handle new user input and generate response."""
    if prompt := st.chat_input("Ask about video games..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            with st.spinner("Thinking..."):
                try:
                    # Get response from ADK agent
                    response = run_async(
                        st.session_state.adk_service.send_message_sync(
                            user_id=st.session_state.user_id,
                            session_id=st.session_state.session_id,
                            message=prompt,
                        )
                    )

                    message_placeholder.markdown(response)

                    # Add to history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )


def main():
    """Main application entry point."""
    initialize_session_state()

    # Header
    st.title("🎮 AI Video Games Assistant")
    st.caption("Your expert companion for all things gaming")

    # Sidebar
    render_sidebar()

    # Chat interface
    render_chat_history()
    handle_user_input()


if __name__ == "__main__":
    main()
