"""Minimal FastAPI wrapper for the ADK fun-facts experiment."""

import json
import uuid

from fastapi import FastAPI, HTTPException, Query
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from fun_facts.agent import root_agent

APP_NAME = "fun_facts"
USER_ID = "api-user"

app = FastAPI(title="fun-facts")


def _strip_code_fences(raw_response: str) -> str:
    """Remove common markdown code fences before JSON parsing."""
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def _parse_facts_json(raw_response: str) -> list[str]:
    """Parse and validate fun-facts JSON, requiring exactly five facts."""
    # Reliability fix: strictly parse JSON (with fence stripping) and validate shape/count.
    cleaned = _strip_code_fences(raw_response)
    payload = json.loads(cleaned)

    if not isinstance(payload, dict):
        raise ValueError("Model response is not a JSON object.")
    facts = payload.get("facts")
    if not isinstance(facts, list):
        raise ValueError("Model response JSON must include a facts list.")

    parsed_facts = [fact.strip() for fact in facts if isinstance(fact, str) and fact.strip()]
    if len(parsed_facts) != 5:
        raise ValueError(f"Expected exactly 5 facts but received {len(parsed_facts)}.")
    return parsed_facts


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
            return _parse_facts_json(response_text)

    raise ValueError("No final response received from model.")


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/fun-fact")
async def fun_fact(topic: str = Query(default="space", min_length=1)) -> dict[str, object]:
    cleaned_topic = topic.strip()
    try:
        facts = await generate_fun_facts(cleaned_topic)
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to generate reliable structured facts: {exc}",
        ) from exc
    return {"topic": cleaned_topic, "facts": facts}
