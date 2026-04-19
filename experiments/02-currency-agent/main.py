"""Minimal FastAPI wrapper for the currency ADK agent."""

import uuid

from fastapi import FastAPI, Query
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from currency_agent import root_agent

APP_NAME = "currency_agent"
USER_ID = "web-user"

app = FastAPI(title="Currency Agent API")


async def ask_currency_agent(prompt: str) -> str:
    """Send one prompt to the ADK agent and return final text."""
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

    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            return "".join(part.text for part in event.content.parts if part.text)

    return "No response received."


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/convert")
async def convert(
    source_currency: str = Query(..., alias="from", min_length=3, max_length=3),
    target_currency: str = Query(..., alias="to", min_length=3, max_length=3),
    amount: float = Query(..., gt=0),
) -> dict:
    source = source_currency.upper()
    target = target_currency.upper()

    prompt = (
        f"Convert {amount} {source} to {target}. "
        "Use the get_exchange_rate tool and include the converted amount."
    )
    answer = await ask_currency_agent(prompt)

    return {
        "ok": True,
        "request": {
            "from": source,
            "to": target,
            "amount": amount,
        },
        "agent_response": answer,
    }
