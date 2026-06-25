"""Chapter 5: Function tools and guarded agent tool use."""

from __future__ import annotations

import asyncio
import os
from typing import Annotated

from agent_framework import Agent, FunctionTool, normalize_tools, tool
from agent_framework.openai import OpenAIChatClient


@tool
def add(
    a: Annotated[int, "left operand"],
    b: Annotated[int, "right operand"] = 1,
) -> int:
    """Add two integers."""
    return a + b


async def main() -> None:
    schema = add.to_dict()
    print(schema["name"], schema["input_model"]["properties"]["a"]["description"])
    print(add(2, b=3))

    invoked = await add.invoke(arguments={"a": 10, "b": 5})
    print(invoked)

    normalized = normalize_tools([add])
    assert isinstance(normalized[0], FunctionTool)

    client = OpenAIChatClient(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY") or "placeholder",
    )
    agent = Agent(client, instructions="Use tools for arithmetic.", tools=[add])

    if not os.getenv("OPENAI_API_KEY"):
        print(f"Constructed agent {agent.name!r} with tool {add.name!r}; skipping live call.")
        return

    # requires OPENAI_API_KEY
    response = await agent.run("What is 10 + 5?")
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
