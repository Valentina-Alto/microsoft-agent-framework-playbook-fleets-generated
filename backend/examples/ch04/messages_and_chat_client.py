"""Chapter 4: Messages, content, options, and guarded chat-client call."""

from __future__ import annotations

import asyncio
import os

from agent_framework import ChatOptions, ChatResponse, Content, Message
from agent_framework.openai import OpenAIChatClient


def build_messages() -> list[Message]:
    return [
        Message("system", ["You are concise."]),
        Message("user", [Content.from_text("Say hello in five words or fewer.")]),
    ]


async def main() -> None:
    messages = build_messages()
    options: ChatOptions = {"temperature": 0.2, "conversation_id": "example-conversation"}
    local_response = ChatResponse(messages=[Message("assistant", ["Hello from local shape."])])
    print(messages[1].text)
    print(local_response.text)

    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping live OpenAIChatClient.get_response call; set OPENAI_API_KEY to run it.")
        return

    # requires OPENAI_API_KEY
    client = OpenAIChatClient(model="gpt-4o-mini", api_key=os.environ["OPENAI_API_KEY"])
    response = await client.get_response(messages, options=options)
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
