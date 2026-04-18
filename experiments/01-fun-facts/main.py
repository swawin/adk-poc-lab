"""Minimal FastAPI wrapper for the ADK fun-facts experiment."""

import json
import uuid

from fastapi import FastAPI, Query
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from fun_facts.agent import root_agent

APP_NAME = "fun_facts"
USER_ID = "api-user"

app = FastAPI(title="fun-facts")


def _normalize_facts(raw_response: str) -> list[str]:
    """Return up to five clean facts, preferring JSON but allowing simple fallback parsing."""
    try:
        payload = json.loads(raw_response)
        if isinstance(payload, dict) and isinstance(payload.get("facts"), list):
            parsed = [str(item).strip() for item in payload["facts"] if str(item).strip()]
            return parsed[:5]
    except json.JSONDecodeError:
        pass

    lines = [line.strip(" -•*\t") for line in raw_response.splitlines() if line.strip()]
    return lines[:5]


async def generate_fun_facts(topic: str) -> list[str]:
    """Generate exactly five topic-specific fun facts using the ADK agent."""
    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Keep the response machine-friendly by asking for compact JSON with five distinct facts.
    prompt = (
        f"Return exactly 5 distinct fun facts about {topic}. "
        'Respond with JSON only in this shape: {"facts": ["fact 1", "fact 2", "fact 3", "fact 4", "fact 5"]}.'
    )
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = "".join(part.text for part in event.content.parts if part.text)
            facts = _normalize_facts(response_text)
            if len(facts) >= 5:
                return facts[:5]
            break

    return [
        f"I couldn't generate fact {index} for {topic} right now."
        for index in range(1, 6)
    ]


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/fun-fact")
async def fun_fact(topic: str = Query(default="space", min_length=1)) -> dict[str, object]:
    cleaned_topic = topic.strip()
    facts = await generate_fun_facts(cleaned_topic)
    return {"topic": cleaned_topic, "facts": facts}
