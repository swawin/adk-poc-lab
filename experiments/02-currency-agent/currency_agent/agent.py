"""Minimal ADK currency agent wired to an MCP tool server."""

import os

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

load_dotenv()

SYSTEM_INSTRUCTION = """
You are a currency conversion assistant.
Use the get_exchange_rate tool for exchange-rate questions.
If a request is unrelated to currencies, politely decline.
""".strip()

root_agent = LlmAgent(
    model=os.getenv("ADK_MODEL", "gemini-2.5-flash"),
    name="currency_agent",
    description="Converts currencies using an MCP exchange-rate tool.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=os.getenv("MCP_SERVER_URL", "http://localhost:8080/mcp")
            )
        )
    ],
)
