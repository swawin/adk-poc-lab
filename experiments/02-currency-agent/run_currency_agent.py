"""Run the minimal currency ADK agent in a local CLI loop.

Before running this script, start the MCP server in another terminal:
  python -m currency_agent.mcp_server
"""

import asyncio
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from currency_agent import root_agent

APP_NAME = "currency_agent"
USER_ID = "local-user"


async def ask_agent(prompt: str) -> str:
    """Send one prompt and return the final model text."""
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


async def main() -> None:
    print("Currency Agent (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        reply = await ask_agent(user_input)
        print(f"Agent: {reply}")


if __name__ == "__main__":
    asyncio.run(main())
