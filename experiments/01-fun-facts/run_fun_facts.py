"""Run the fun-facts ADK agent as a plain Python script.

Example:
  python run_fun_facts.py "octopuses"
"""

import asyncio
import sys
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from fun_facts.agent import root_agent

APP_NAME = "fun_facts"
USER_ID = "local-user"


async def main() -> None:
    topic = " ".join(sys.argv[1:]).strip() or "space"

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

    print(f"Topic: {topic}\n")
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)
            break


if __name__ == "__main__":
    asyncio.run(main())
