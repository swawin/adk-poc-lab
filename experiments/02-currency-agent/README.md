# 02 Currency Agent

A minimal learning adaptation of the Google ADK `currency-agent` sample.

## What this sample does

This experiment creates an ADK agent that answers currency-conversion questions.
Instead of hardcoding rates, it calls a tool named `get_exchange_rate` through MCP.
The tool is served by a small local MCP server that fetches real rates from frankfurter.app.

## Files created

- `currency_agent/agent.py` - ADK `LlmAgent` definition + MCP tool wiring
- `currency_agent/mcp_server.py` - minimal MCP server exposing `get_exchange_rate`
- `currency_agent/__init__.py` - package export for `root_agent`
- `run_currency_agent.py` - simple CLI runner for learning and local testing
- `requirements.txt` - minimal dependencies needed for this experiment

## How it works (high level)

1. `mcp_server.py` starts an MCP HTTP server and registers `get_exchange_rate`.
2. `agent.py` creates a `LlmAgent` and attaches `MCPToolset` pointing to that server.
3. `run_currency_agent.py` sends user prompts to the ADK runner.
4. For currency questions, the agent calls the MCP tool and returns a final answer.

## Run locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your model credentials (example with Google AI Studio key):

```bash
export GOOGLE_API_KEY=your_key_here
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

3. Start MCP server (terminal 1):

```bash
python -m currency_agent.mcp_server
```

4. Run agent CLI (terminal 2):

```bash
python run_currency_agent.py
```

This is intentionally a simple POC for learning ADK structure and tool integration.
