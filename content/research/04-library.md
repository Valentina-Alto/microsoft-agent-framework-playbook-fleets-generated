# Chapter 4 library notes: Chat clients, messages, and conversations

Inspected version: `agent-framework==1.9.0` (`agent-framework-core==1.9.0`). Introspection used `inspect.signature`, docstrings, and import probes against the installed package.

## `BaseChatClient` / `agent_framework.BaseChatClient`

Implements concept: provider-independent chat client abstraction that accepts normalized messages/options and returns normalized chat responses.

Real signatures:

```python
BaseChatClient(
    *,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    additional_properties: dict[str, Any] | None = None,
) -> None

BaseChatClient.get_response(
    self,
    messages: Sequence[Message],
    *,
    stream: bool = False,
    options: OptionsCoT | ChatOptions[Any] | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    function_invocation_kwargs: Mapping[str, Any] | None = None,
    client_kwargs: Mapping[str, Any] | None = None,
) -> Awaitable[ChatResponse[Any]] | ResponseStream[ChatResponseUpdate, ChatResponse[Any]]
```

`BaseChatClient` is an abstract base for chat clients without the full public middleware wrapping. Its docstring says subclasses implement `_inner_get_response()` and public clients such as `OpenAIChatClient` compose the layers normally needed by applications.

Surprise from introspection: the top-level public API did not expose a symbol named `ChatClientProtocol`; the relevant public protocol-like name is `SupportsChatGetResponse`, alongside `BaseChatClient` and `TokenizerProtocol`.

When to use: target `BaseChatClient`/`SupportsChatGetResponse` in abstractions and tests. When not to use: do not instantiate it directly; use a concrete provider client.

Minimal example: `backend/examples/ch04/messages_and_chat_client.py`.

## `OpenAIChatClient` and `OpenAIChatCompletionClient` / `agent_framework.openai`

Implements concept: concrete chat clients for OpenAI-compatible Responses API and Chat Completions API.

Real signatures:

```python
OpenAIChatClient(
    model: str | None = None,
    *,
    api_key: str | Callable[[], str | Awaitable[str]] | None = None,
    credential: AzureCredentialTypes | AzureTokenProvider | None = None,
    org_id: str | None = None,
    base_url: str | None = None,
    azure_endpoint: str | None = None,
    api_version: str | None = None,
    default_headers: Mapping[str, str] | None = None,
    async_client: AsyncOpenAI | None = None,
    instruction_role: str | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    middleware: Sequence[ChatAndFunctionMiddlewareTypes] | None = None,
    function_invocation_configuration: FunctionInvocationConfiguration | None = None,
    additional_properties: dict[str, Any] | None = None,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
) -> None

OpenAIChatCompletionClient(
    model: str | None = None,
    *,
    api_key: str | Callable[[], str | Awaitable[str]] | None = None,
    credential: AzureCredentialTypes | AzureTokenProvider | None = None,
    org_id: str | None = None,
    default_headers: Mapping[str, str] | None = None,
    async_client: AsyncOpenAI | None = None,
    instruction_role: str | None = None,
    base_url: str | None = None,
    azure_endpoint: str | None = None,
    api_version: str | None = None,
    middleware: Sequence[ChatAndFunctionMiddlewareTypes] | None = None,
    function_invocation_configuration: FunctionInvocationConfiguration | None = None,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
) -> None
```

`OpenAIChatClient` is documented as an OpenAI Responses client with middleware, telemetry, and function invocation support. `OpenAIChatCompletionClient` is the analogous Chat Completions client. Both expose `get_response(messages, stream=False, options=..., ...)` and can also be supplied to `Agent`.

When to use: use `OpenAIChatClient` for new OpenAI Responses API-style work and `OpenAIChatCompletionClient` when you specifically need Chat Completions behavior. When not to use: do not use `RawOpenAI*` clients unless composing your own layers; their docstrings warn they omit middleware, telemetry, and function invocation support.

Minimal example: `backend/examples/ch04/messages_and_chat_client.py` (`# requires OPENAI_API_KEY` for live call).

## `FoundryChatClient` and `FoundryAgent` / `agent_framework.foundry`

Implements concept: Azure AI Foundry-backed chat and hosted/prompt agent integration.

Real signatures:

```python
FoundryChatClient(
    *,
    project_endpoint: str | None = None,
    project_client: AIProjectClient | None = None,
    model: str | None = None,
    credential: AzureCredentialTypes | AzureTokenProvider | None = None,
    allow_preview: bool | None = None,
    default_headers: Mapping[str, str] | None = None,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
    instruction_role: str | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    additional_properties: dict[str, Any] | None = None,
    middleware: Sequence[ChatAndFunctionMiddlewareTypes] | None = None,
    function_invocation_configuration: FunctionInvocationConfiguration | None = None,
) -> None

FoundryAgent(
    *,
    project_endpoint: str | None = None,
    agent_name: str | None = None,
    agent_version: str | None = None,
    credential: AzureCredentialTypes | None = None,
    project_client: AIProjectClient | None = None,
    allow_preview: bool | None = None,
    default_headers: Mapping[str, str] | None = None,
    tools: FunctionTool | Callable[..., Any] | Sequence[FunctionTool | Callable[..., Any]] | None = None,
    context_providers: Sequence[ContextProvider] | None = None,
    middleware: Sequence[MiddlewareTypes] | None = None,
    client_type: type[RawFoundryAgentChatClient] | None = None,
    env_file_path: str | None = None,
    env_file_encoding: str | None = None,
    id: str | None = None,
    name: str | None = None,
    description: str | None = None,
    instructions: str | None = None,
    default_options: FoundryAgentOptionsT | Mapping[str, Any] | None = None,
    require_per_service_call_history_persistence: bool = False,
    function_invocation_configuration: FunctionInvocationConfiguration | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    additional_properties: Mapping[str, Any] | None = None,
    timeout: float | None = None,
) -> None

FoundryAgent.run(
    self,
    messages: AgentRunInputs | None = None,
    *,
    stream: bool = False,
    session: AgentSession | None = None,
    middleware: Sequence[MiddlewareTypes] | None = None,
    tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None = None,
    options: ChatOptions[Any] | None = None,
    compaction_strategy: CompactionStrategy | None = None,
    tokenizer: TokenizerProtocol | None = None,
    function_invocation_kwargs: Mapping[str, Any] | None = None,
    client_kwargs: Mapping[str, Any] | None = None,
) -> Awaitable[AgentResponse[Any]] | ResponseStream[AgentResponseUpdate, AgentResponse[Any]]
```

The installed `agent_framework.foundry` module exposes `FoundryChatClient`, `FoundryAgent`, raw variants, `FoundryLocalClient`, and Foundry options. `FoundryChatClient` uses a Foundry project endpoint and model deployment. `FoundryAgent` connects to an existing PromptAgent or HostedAgent and has the same `run(..., stream=False, session=..., tools=...)` shape as `Agent`.

When to use: use Foundry classes when your deployment is in Azure AI Foundry or you need hosted/prompt agents. When not to use: avoid them for local/import-only examples unless credentials and Foundry project configuration are available.

Minimal example: `backend/examples/ch04/messages_and_chat_client.py` mentions provider swap but does not instantiate Foundry to avoid credential requirements.

## `agent_framework.azure` provider-adjacent module

Implements concept: Azure-hosted state, durable execution, function-app hosting, and search context providers rather than a basic chat-client abstraction.

Public classes found by introspection included `AgentFunctionApp`, `AzureAISearchContextProvider`, `CosmosHistoryProvider`, `DurableAIAgent`, `DurableAIAgentClient`, `DurableAIAgentOrchestrationContext`, and `DurableAIAgentWorker`. Representative real signatures:

```python
AgentFunctionApp(
    agents: list[SupportsAgentRun] | None = None,
    workflow: Workflow | None = None,
    http_auth_level: func.AuthLevel = AuthLevel.FUNCTION,
    enable_health_check: bool = True,
    enable_http_endpoints: bool = True,
    max_poll_retries: int = 30,
    poll_interval_seconds: float = 1.0,
    enable_mcp_tool_trigger: bool = False,
    default_callback: AgentResponseCallbackProtocol | None = None,
)

AzureAISearchContextProvider(
    source_id: str = "azure_ai_search",
    endpoint: str | None = None,
    index_name: str | None = None,
    api_key: str | AzureKeyCredential | None = None,
    credential: AzureCredentialTypes | None = None,
    *,
    mode: Literal["semantic", "agentic"] = "semantic",
    top_k: int = 5,
    ...
) -> None
```

Use these when the chapter needs Azure Functions/Durable Agent hosting or Azure AI Search context rather than direct chat calls. Do not present `agent_framework.azure` as the OpenAI/Azure OpenAI chat-client import path in this installed version; OpenAI-compatible client classes are under `agent_framework.openai`, while Foundry chat/agent classes are under `agent_framework.foundry`.

## `Message`, `Content`, and `RoleLiteral` / `agent_framework`

Implements concept: normalized conversation turns and multimodal/tool content.

Real signatures:

```python
Message(
    role: RoleLiteral | str,
    contents: Sequence[Content | str | Mapping[str, Any]] | None = None,
    *,
    author_name: str | None = None,
    message_id: str | None = None,
    additional_properties: MutableMapping[str, Any] | None = None,
    raw_representation: Any | None = None,
) -> None

Content(
    type: ContentType,
    *,
    text: str | None = None,
    protected_data: str | None = None,
    uri: str | None = None,
    media_type: str | None = None,
    ...
) -> None

Content.from_text(text: str, *, annotations=None, additional_properties=None, raw_representation=None) -> ContentT
Content.from_uri(uri: str, *, media_type: str | None = None, annotations=None, additional_properties=None, raw_representation=None) -> ContentT
Content.from_function_call(call_id: str, name: str, *, arguments: str | Mapping[str, Any] | None = None, ...) -> ContentT
Content.from_function_result(call_id: str, *, result: Any = None, exception: str | None = None, ...) -> ContentT

RoleLiteral = Literal["system", "user", "assistant", "tool"]
```

There is no public `TextContent` class in the inspected top-level API; `Content` is a unified content container with factory methods such as `from_text`, `from_uri`, `from_function_call`, and `from_function_result`. `Message` takes a role string/literal and a sequence of strings, `Content` objects, or content mappings.

When to use: use `Message("user", ["..."])` and `Content.from_*` to build provider-neutral chat history. When not to use: do not rely on provider raw message shapes unless writing an adapter.

Minimal example: `backend/examples/ch04/messages_and_chat_client.py`.

## `ChatResponse`, `ChatResponseUpdate`, `ChatOptions`, and conversation IDs / `agent_framework`

Implements concept: normalized chat completion outputs, streaming chunks, and request options including conversation state hints.

Real signatures:

```python
ChatResponse(
    *,
    messages: Message | Sequence[Message] | None = None,
    response_id: str | None = None,
    conversation_id: str | None = None,
    model: str | None = None,
    created_at: CreatedAtT | None = None,
    finish_reason: FinishReasonLiteral | FinishReason | None = None,
    usage_details: UsageDetails | None = None,
    value: ResponseModelT | None = None,
    response_format: StructuredResponseFormat = None,
    continuation_token: ContinuationToken | None = None,
    additional_properties: dict[str, Any] | None = None,
    raw_representation: Any | None = None,
) -> None

ChatResponseUpdate(
    *,
    contents: Sequence[Content] | None = None,
    role: RoleLiteral | Role | None = None,
    author_name: str | None = None,
    response_id: str | None = None,
    message_id: str | None = None,
    conversation_id: str | None = None,
    model: str | None = None,
    created_at: CreatedAtT | None = None,
    finish_reason: FinishReasonLiteral | FinishReason | None = None,
    continuation_token: ContinuationToken | None = None,
    additional_properties: dict[str, Any] | None = None,
    raw_representation: Any | None = None,
) -> None

ChatOptions = TypedDict(total=False) with keys including:
model, temperature, top_p, max_tokens, stop, seed, tools, tool_choice,
allow_multiple_tool_calls, response_format, metadata, user, store,
conversation_id, instructions
```

`ChatResponse` carries returned `Message` objects, provider/model metadata, and an optional `conversation_id`. `ChatOptions` is a common optional `TypedDict`; conversation/multi-turn state can be represented explicitly by passing prior `Message` objects, by passing provider conversation IDs in options, and at the agent level by `AgentSession`.

When to use: use `ChatResponse` for direct client calls and `ChatOptions` for provider-independent settings. When not to use: avoid assuming all providers honor every `ChatOptions` key; provider-specific option TypedDicts extend the common set.

Minimal example: `backend/examples/ch04/messages_and_chat_client.py`.
