"""
ADK Service for Streamlit Integration

This module provides session management for the ADK agent,
ensuring persistence across Streamlit reruns.
"""

import asyncio
from typing import Optional, AsyncGenerator
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types

from my_agent.agent import root_agent


class ADKService:
    """
    Singleton service to manage ADK Runner and Sessions.
    Ensures the runner persists across Streamlit script reruns.
    """

    _instance: Optional["ADKService"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not ADKService._initialized:
            self._session_service = InMemorySessionService()
            self._runner = Runner(
                agent=root_agent,
                app_name="videogames_assistant",
                session_service=self._session_service,
            )
            self._sessions: dict[str, Session] = {}
            ADKService._initialized = True

    async def get_or_create_session(
        self, user_id: str, session_id: str
    ) -> Session:
        """Get existing session or create new one."""
        key = f"{user_id}:{session_id}"

        if key not in self._sessions:
            session = await self._session_service.create_session(
                app_name="videogames_assistant",
                user_id=user_id,
                session_id=session_id,
                state={"preferences": {}},
            )
            self._sessions[key] = session

        return self._sessions[key]

    async def send_message(
        self, user_id: str, session_id: str, message: str
    ) -> AsyncGenerator[str, None]:
        """
        Send a message to the agent and stream the response.

        Yields chunks of the response as they are generated.
        """
        await self.get_or_create_session(user_id, session_id)

        user_content = types.Content(
            role="user", parts=[types.Part(text=message)]
        )

        async for event in self._runner.run_async(
            user_id=user_id, session_id=session_id, new_message=user_content
        ):
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        yield part.text

    async def send_message_sync(
        self, user_id: str, session_id: str, message: str
    ) -> str:
        """Send message and return complete response (non-streaming)."""
        response_parts = []
        async for chunk in self.send_message(user_id, session_id, message):
            response_parts.append(chunk)
        return "".join(response_parts)


def get_adk_service() -> ADKService:
    """Factory function to get the singleton ADK service."""
    return ADKService()
