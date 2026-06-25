# Chapter 3 library notes: Agents and instructions

Inspected version: `agent-framework==1.9.0` (`agent-framework-core==1.9.0`). Introspection used `inspect.signature`, docstrings, and import probes against the installed package.

## `Agent` / `agent_framework.Agent`

Implements concept: the agent as an instruction-bound runnable that wraps a chat client, tool set, middleware, context providers, and per-run/session state.

Real signatures:

```python
Agent(
    client: SupportsChatGetResponse[OptionsCoT],
    instructions: str | None = None,
    *,
    id: str | None = None,
    name: str | None = None,
    description: str | None = None,
    tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None = None,
    default_options: OptionsCoT | None = None,
    context_providers: Sequence[ContextProvider] | None = None,
    middleware: Sequence[MiddlewareTypes] | None = None,
    require_per_service_call_history_persistence: bool = False,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    additional_properties: MutableMapping[str, Any] | None = None,
) -> None

Agent.run(
    self,
    messages: AgentRunInputs | None = None,
    *,
    stream: bool = False,
    session: AgentSession | None = None,
    middleware: Sequence[MiddlewareTypes] | None = None,
    tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None = None,
    options: OptionsCoT | ChatOptions[Any] | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    function_invocation_kwargs: Mapping[str, Any] | None = None,
    client_kwargs: Mapping[str, Any] | None = None,
) -> Awaitable[AgentResponse[Any]] | ResponseStream[AgentResponseUpdate, AgentResponse[Any]]

Agent.as_tool(
    self,
    *,
    name: str | None = None,
    description: str | None = None,
    arg_name: str = "task",
    arg_description: str | None = None,
    approval_mode: Literal["always_require", "never_require"] = "never_require",
    stream_callback: Callable[[AgentResponseUpdate], Awaitable[None] | None] | None = None,
    propagate_session: bool = False,
) -> FunctionTool
```

`Agent` is the recommended concrete chat-client agent: its docstring says it adds middleware, telemetry, and full layer support over a chat client. The `instructions` constructor parameter is the durable persona/system guidance for the agent; `messages` passed to `run` are the current task or conversation input. There is no separate `run_stream` method in 1.9.0; streaming is selected with `run(..., stream=True)` and returns a `ResponseStream` over `AgentResponseUpdate` chunks.

When to use: use `Agent` for normal application agents where you want instructions, tools, middleware, telemetry, and provider-independent invocation. When not to use: do not use it if you are implementing a custom low-level agent loop or client; use `BaseAgent`/provider clients directly only for extension points.

Minimal example: `backend/examples/ch03/agent_run_structure.py`.

```python
import os
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY") or "placeholder")
agent = Agent(client, instructions="Answer concisely.", name="concise-assistant")
# requires OPENAI_API_KEY to actually call the model:
# response = await agent.run("Explain agents in one sentence.")
```

## `BaseAgent` / `agent_framework.BaseAgent`

Implements concept: the abstract base contract and shared session/context plumbing for custom agent implementations.

Real signatures:

```python
BaseAgent(
    *,
    id: str | None = None,
    name: str | None = None,
    description: str | None = None,
    context_providers: Sequence[ContextProvider] | None = None,
    middleware: Sequence[MiddlewareTypes] | None = None,
    additional_properties: MutableMapping[str, Any] | None = None,
) -> None
```

`BaseAgent` is documented as the minimal base class for all Agent Framework agents. It cannot be instantiated directly because it does not implement `run`; subclasses must provide the invocation behavior. It still supplies core metadata, context-provider, middleware, and `as_tool(...)` behavior.

When to use: use only when building a custom agent type or adapter. When not to use: prefer `Agent` for ordinary chat-client agents.

Minimal example: see `backend/examples/ch03/agent_run_structure.py` for the normal `Agent` path.

## `AgentResponse` and `AgentResponseUpdate` / `agent_framework.AgentResponse`, `agent_framework.AgentResponseUpdate`

Implements concept: normalized final and streaming outputs from an agent run.

Real signatures:

```python
AgentResponse(
    *,
    messages: Message | Sequence[Message] | None = None,
    response_id: str | None = None,
    agent_id: str | None = None,
    created_at: CreatedAtT | None = None,
    finish_reason: FinishReasonLiteral | FinishReason | None = None,
    usage_details: UsageDetails | None = None,
    value: ResponseModelT | None = None,
    response_format: StructuredResponseFormat = None,
    continuation_token: ContinuationToken | None = None,
    raw_representation: Any | None = None,
    additional_properties: dict[str, Any] | None = None,
) -> None

AgentResponseUpdate(
    *,
    contents: Sequence[Content] | None = None,
    role: RoleLiteral | str | None = None,
    author_name: str | None = None,
    agent_id: str | None = None,
    response_id: str | None = None,
    message_id: str | None = None,
    created_at: CreatedAtT | None = None,
    finish_reason: FinishReasonLiteral | FinishReason | None = None,
    continuation_token: ContinuationToken | None = None,
    additional_properties: dict[str, Any] | None = None,
    raw_representation: Any | None = None,
) -> None
```

`AgentResponse` contains one or more `Message` objects plus metadata such as finish reason, usage, structured `value`, and continuation token. `AgentResponseUpdate` is the chunk type emitted by streaming agent runs.

When to use: read `response.text`/`response.messages` from final runs and consume updates for streaming UIs. When not to use: do not construct provider-specific response objects in application code unless writing a provider adapter.

Minimal example: `backend/examples/ch03/agent_run_structure.py` creates a local `AgentResponse` without a live LLM call.

## `AgentSession` / `agent_framework.AgentSession`

Implements concept: multi-turn agent-side conversation/session state.

Real signature:

```python
AgentSession(*, session_id: str | None = None, service_session_id: str | None = None)
```

`AgentSession` is a lightweight state container. Its docstring says provider instances are owned by the agent, not the session; the session holds session IDs plus a mutable `state` dict shared with providers and middleware.

When to use: pass the same `AgentSession` into repeated `agent.run(...)` calls when the agent/provider/middleware needs session continuity. When not to use: simple one-shot calls can omit it.

Minimal example: `backend/examples/ch03/agent_run_structure.py`.
