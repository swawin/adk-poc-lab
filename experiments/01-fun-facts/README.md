# 01-fun-facts

A minimal learning adaptation of Google's ADK `fun-facts` sample, now with a tiny FastAPI web wrapper.

## What this sample does

This experiment defines a small ADK agent that answers with surprising fun facts on any topic.
It follows the same core ADK pattern as the reference sample:

- load environment variables
- define a root `Agent`
- attach the built-in `google_search` tool
- expose a very small HTTP API for browser/phone testing

## Files

- `fun_facts/agent.py` – root agent + ADK `App` definition
- `fun_facts/__init__.py` – package exports for easy imports
- `run_fun_facts.py` – simple script entrypoint to run the agent directly from Python
- `main.py` – FastAPI app entrypoint for local web/API usage
- `requirements.txt` – minimal dependencies for this experiment

## Run the web app

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set credentials/environment values expected by ADK/Gemini (for example in a local `.env`).
4. Start the API server:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. Test endpoints:

   - Health check: `http://localhost:8000/health`
   - Fun fact: `http://localhost:8000/fun-fact?topic=space`

Cross-origin frontend calls are supported via FastAPI CORS middleware for:

- `http://localhost:5173`
- `http://localhost:3000`
- `https://*.vercel.app` (via origin regex)

API response shape for `GET /fun-fact?topic=space` (topic can be any value):

```json
{
  "topic": "space",
  "facts": [
    "fact 1",
    "fact 2",
    "fact 3",
    "fact 4",
    "fact 5"
  ]
}
```

The endpoint now validates structured JSON from the model, strips markdown code fences when needed, and only returns a response when exactly 5 facts are present.


## Optional script mode

You can still run the original script entrypoint:

```bash
python run_fun_facts.py "volcanoes"
```

If no topic is provided, the script defaults to `space`.

---

This is intentionally a POC learning setup (simple, readable, minimal), not a production-ready app.
