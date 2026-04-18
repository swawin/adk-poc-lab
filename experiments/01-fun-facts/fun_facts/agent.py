"""Minimal ADK fun-facts agent.

This mirrors the official ADK sample pattern:
- load environment variables
- define a root Agent
- optionally expose an App object for ADK CLI
"""

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools import google_search

load_dotenv(override=True)

root_agent = Agent(
    name="Facts",
    model="gemini-2.0-flash",
    instruction=(
        "Provide mind-blowing, obscure, and wacky fun facts about the topic. "
        "Keep facts concise, surprising, and easy to understand."
    ),
    description="An agent that shares surprising fun facts about a topic.",
    tools=[google_search],
)

app = App(name="fun_facts", root_agent=root_agent)
