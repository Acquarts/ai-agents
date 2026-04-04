#!/usr/bin/env python3
"""Entry point for the AI news pipeline. Run this directly or via Task Scheduler."""
import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import OrchestratorAgent

if __name__ == "__main__":
    OrchestratorAgent().run()
