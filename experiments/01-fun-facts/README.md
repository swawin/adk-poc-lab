# 01-fun-facts

A minimal learning adaptation of Google's ADK `fun-facts` sample.

## What this sample does

This experiment defines a small ADK agent that answers with surprising fun facts on any topic.
It follows the same core ADK pattern as the reference sample:

- load environment variables
- define a root `Agent`
- attach the built-in `google_search` tool
- optionally expose an `App` object

## Files created

- `fun_facts/agent.py` – root agent + ADK `App` definition
- `fun_facts/__init__.py` – package exports for easy imports
- `run_fun_facts.py` – simple script entrypoint to run the agent directly from Python
- `requirements.txt` – minimal dependencies for this experiment

## High-level run steps

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set credentials/environment values expected by ADK/Gemini (for example in a local `.env`).
4. Run the script with a topic:

   ```bash
   python run_fun_facts.py "volcanoes"
   ```

If no topic is provided, the script defaults to `space`.

---

This is intentionally a POC learning setup (simple, readable, minimal), not a production-ready app.
