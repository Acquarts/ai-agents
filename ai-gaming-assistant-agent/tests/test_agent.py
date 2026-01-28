"""
Tests for the AI Video Games Assistant agent.
"""

import pytest


class TestAgentStructure:
    """Tests for verifying agent structure and configuration."""

    def test_root_agent_exists(self):
        """Test that root_agent can be imported."""
        from my_agent.agent import root_agent

        assert root_agent is not None

    def test_root_agent_name(self):
        """Test that root_agent has correct name."""
        from my_agent.agent import root_agent

        assert root_agent.name == "Videogames_Assistant"

    def test_root_agent_model(self):
        """Test that root_agent uses correct model."""
        from my_agent.agent import root_agent

        assert root_agent.model == "gemini-2.5-flash"

    def test_root_agent_has_sub_agents(self):
        """Test that root_agent has sub-agents configured."""
        from my_agent.agent import root_agent

        assert root_agent.sub_agents is not None
        assert len(root_agent.sub_agents) > 0

    def test_root_agent_has_tools(self):
        """Test that root_agent has tools configured."""
        from my_agent.agent import root_agent

        assert root_agent.tools is not None
        assert len(root_agent.tools) > 0

    def test_youtube_searching_agent_exists(self):
        """Test that youtube_searching sub-agent exists."""
        from my_agent.agent import youtube_searching

        assert youtube_searching is not None
        assert youtube_searching.name == "youtube_searching"


class TestPackageExports:
    """Tests for verifying package exports."""

    def test_package_exports_root_agent(self):
        """Test that my_agent package exports root_agent."""
        from my_agent import root_agent

        assert root_agent is not None


class TestADKService:
    """Tests for the ADK service."""

    def test_adk_service_singleton(self):
        """Test that ADKService is a singleton."""
        from app.adk_service import get_adk_service

        service1 = get_adk_service()
        service2 = get_adk_service()

        assert service1 is service2

    def test_adk_service_has_runner(self):
        """Test that ADKService has a runner configured."""
        from app.adk_service import get_adk_service

        service = get_adk_service()

        assert hasattr(service, "_runner")
        assert service._runner is not None


class TestObservability:
    """Tests for observability module."""

    def test_setup_tracing_function_exists(self):
        """Test that setup_tracing function exists."""
        from observability.tracing import setup_tracing

        assert callable(setup_tracing)

    def test_setup_tracing_idempotent(self):
        """Test that setup_tracing can be called multiple times safely."""
        from observability.tracing import setup_tracing

        # Should not raise any exceptions
        setup_tracing()
        setup_tracing()
