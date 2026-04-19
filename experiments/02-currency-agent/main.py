"""Minimal FastAPI wrapper for the currency ADK agent."""

import logging
import traceback
import uuid
from typing import Any

from fastapi import FastAPI, Query
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from currency_agent import root_agent

APP_NAME = "currency_agent"
USER_ID = "web-user"
MAX_DEBUG_EVENTS = 8

app = FastAPI(title="Currency Agent API")
logger = logging.getLogger(__name__)


def _event_to_debug(event: Any) -> dict[str, Any]:
    """Build a compact event snapshot for troubleshooting."""
    parts = []
    content = getattr(event, "content", None)
    for part in getattr(content, "parts", []) or []:
        text = getattr(part, "text", None)
        if text:
            parts.append(text[:200])

    return {
        "type": type(event).__name__,
        "is_final_response": bool(getattr(event, "is_final_response", lambda: False)()),
        "author": getattr(event, "author", None),
        "has_content": bool(content),
        "text_parts": parts,
    }


async def ask_currency_agent(prompt: str) -> dict[str, Any]:
    """Send one prompt to the ADK agent and return structured result + debug info."""
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
    recent_events: list[dict[str, Any]] = []

    try:
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content,
        ):
            # Final text response means the model produced user-facing answer content.
            # Tool/error events are still useful for debug but may not contain final text.
            debug_event = _event_to_debug(event)
            recent_events.append(debug_event)
            recent_events = recent_events[-MAX_DEBUG_EVENTS:]

            if event.is_final_response() and event.content and event.content.parts:
                answer = "".join(part.text for part in event.content.parts if part.text)
                if answer.strip():
                    return {
                        "ok": True,
                        "response": answer,
                        "debug": {"recent_events": recent_events},
                    }
    except Exception as exc:  # Learning POC: keep full exception details visible.
        logger.exception("Currency agent run failed: %s", exc)
        return {
            "ok": False,
            "error_summary": f"{type(exc).__name__}: {exc}",
            "debug": {
                "traceback": traceback.format_exc(),
                "recent_events": recent_events,
            },
        }

    return {
        "ok": False,
        "error_summary": "No final text response received from ADK runner.",
        "debug": {
            "hint": (
                "Runner produced no final user-facing text event. "
                "Inspect recent events to determine whether only tool/error/internal events occurred."
            ),
            "recent_events": recent_events,
        },
    }


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
    result = await ask_currency_agent(prompt)

    response: dict[str, Any] = {
        "request": {
            "from": source,
            "to": target,
            "amount": amount,
            "prompt": prompt,
        }
    }
    if result["ok"]:
        response.update(
            {
                "ok": True,
                "agent_response": result["response"],
            }
        )
        return response

    response.update(
        {
            "ok": False,
            "error_summary": result.get("error_summary", "Unknown agent failure."),
        }
    )
    if "debug" in result:
        response["debug"] = result["debug"]
    return response
