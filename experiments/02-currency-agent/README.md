# 02 Currency Agent

A minimal learning adaptation of the Google ADK `currency-agent` sample.

## What this sample does

This experiment creates an ADK agent that answers currency-conversion questions.
Instead of hardcoding rates, it calls a tool named `get_exchange_rate` through MCP.
The tool is served by a small local MCP server that fetches real rates from frankfurter.app.

## Files

- `currency_agent/agent.py` - ADK `LlmAgent` definition + MCP tool wiring
- `currency_agent/mcp_server.py` - minimal MCP server exposing `get_exchange_rate`
- `run_currency_agent.py` - simple CLI runner for local testing
- `main.py` - FastAPI wrapper with deployable HTTP endpoints
- `requirements.txt` - dependencies for this experiment

## Run as a web service

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set model credentials (example with Google AI Studio key):

```bash
export GOOGLE_API_KEY=your_key_here
export GOOGLE_GENAI_USE_VERTEXAI=FALSE
```

3. Start MCP server (terminal 1):

```bash
python -m currency_agent.mcp_server
```

4. Start FastAPI app (terminal 2):

```bash
uvicorn main:app --reload --port 8000
```

5. Test in browser:

- `http://localhost:8000/health`
- `http://localhost:8000/convert?from=USD&to=EUR&amount=100`

This is intentionally a simple POC for learning ADK + MCP integration.
