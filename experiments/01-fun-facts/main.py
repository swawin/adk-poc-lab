"""Minimal FastAPI wrapper for the ADK fun-facts experiment."""

import uuid

from fastapi import FastAPI, Query
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from fun_facts.agent import root_agent

APP_NAME = "fun_facts"
USER_ID = "api-user"

app = FastAPI(title="fun-facts")


async def generate_fun_fact(topic: str) -> str:
    """Generate a fun fact response for a topic using the ADK agent."""
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

    prompt = f"Share 5 surprising fun facts about {topic}."
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            return event.content.parts[0].text

    return "I couldn't generate a fun fact right now."


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/fun-fact")
async def fun_fact(topic: str = Query(default="space", min_length=1)) -> dict[str, str]:
    fact = await generate_fun_fact(topic.strip())
    return {"topic": topic, "fun_fact": fact}
