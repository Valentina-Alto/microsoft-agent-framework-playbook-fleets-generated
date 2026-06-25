"""Chapter 3: Agent construction and guarded invocation.

This file imports and constructs framework objects without making a live LLM call
unless OPENAI_API_KEY is set.
"""

from __future__ import annotations

import asyncio
import os

from agent_framework import Agent, AgentResponse, AgentSession, Message
from agent_framework.openai import OpenAIChatClient


def build_agent() -> Agent:
    """Create an Agent around an OpenAI chat client.

    # requires OPENAI_API_KEY for real network calls
    """
    client = OpenAIChatClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY") or "placeholder",
    )
    return Agent(
        client,
        instructions="Answer in one concise paragraph.",
        name="concise-assistant",
    )


async def main() -> None:
    agent = build_agent()
    session = AgentSession(session_id="example-session")

    local_response = AgentResponse(messages=[Message("assistant", ["Local response shape."])])
    print(local_response.text)

    if not os.getenv("OPENAI_API_KEY"):
        print(f"Constructed {agent.name!r} with session {session.session_id!r}; skipping live call.")
        return

    # requires OPENAI_API_KEY
    response = await agent.run("Explain what an Agent is in one sentence.", session=session)
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
