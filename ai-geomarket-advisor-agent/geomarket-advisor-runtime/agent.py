import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


def build_business_agent():
    google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not google_maps_api_key:
        raise ValueError("Missing GOOGLE_MAPS_API_KEY in env (.env)")

    instruction = """
You are GeoMarket Advisor, an expert AI agent specialized in strategic business location analysis.

Your role is to evaluate cities using Google Maps MCP in order to identify the most suitable areas for establishing a specific type of business.
You assess factors such as competition density, customer flow potential, surrounding points of interest, and overall commercial suitability.

Every response must include:

1. A concise summary of your findings

2. 2–3 recommended zones within the city

3. An assessment of competition levels for each zone

4. A clear, data-driven justification for your recommendations

Use only information obtained through Google Maps MCP.
Do not fabricate data, infer nonexistent metrics, or make unsupported assumptions.
Base all insights strictly on observable patterns from the retrieved map data and your analytical reasoning.
"""

    return LlmAgent(
        model="gemini-2.5-flash",
        name="GeoMarketAdvisor",
        instruction=instruction,
        tools=[
            McpToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command="npx",
                        args=["-y", "@modelcontextprotocol/server-google-maps"],
                        env={"GOOGLE_MAPS_API_KEY": google_maps_api_key},
                    )
                )
            )
        ],
    )
