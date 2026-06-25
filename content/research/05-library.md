# Chapter 5 library notes: Tools and function calling

Inspected version: `agent-framework==1.9.0` (`agent-framework-core==1.9.0`). Introspection used `inspect.signature`, docstrings, source/docstring probes, and a local `@tool` schema/invocation probe.

## `tool` decorator / `agent_framework.tool`

Implements concept: converting Python functions into model-callable tools/functions with JSON-schema parameters.

Real signature:

```python
tool(
    func: Callable[..., Any] | None = None,
    *,
    name: str | None = None,
    description: str | None = None,
    schema: type[BaseModel] | Mapping[str, Any] | None = None,
    approval_mode: ApprovalMode | None = None,
    kind: str | None = None,
    max_invocations: int | None = None,
    max_invocation_exceptions: int | None = None,
    additional_properties: dict[str, Any] | None = None,
    result_parser: Callable[[Any], str | list[Content]] | _SkipParsingSentinel | None = None,
) -> FunctionTool | Callable[[Callable[..., Any]], FunctionTool]
```

The public decorator is named `tool`, not `ai_function`. Its docstring says it creates a `FunctionTool`, builds a Pydantic model from the Python function signature, validates model-provided arguments, and generates JSON schema. Parameter descriptions can be supplied with `typing.Annotated[..., "description"]` or Pydantic `Field`.

When to use: use `@tool` for the normal “Python function becomes an agent tool” path. When not to use: do not use it for declaration-only tools without an implementation; instantiate `FunctionTool(func=None, input_model=...)` directly for that pattern.

Minimal example: `backend/examples/ch05/tools_function_calling.py`.

```python
from typing import Annotated
from agent_framework import tool

@tool
def add(a: Annotated[int, "left operand"], b: Annotated[int, "right operand"] = 1) -> int:
    """Add two integers."""
    return a + b

print(add.to_dict())  # includes type='function_tool' and generated input_model schema
```

## `FunctionTool` / `agent_framework.FunctionTool`

Implements concept: runtime wrapper for a callable tool, including metadata, input schema, validation, invocation limits, approvals, and serialization.

Real signatures:

```python
FunctionTool(
    *,
    name: str,
    description: str = "",
    approval_mode: ApprovalMode | None = None,
    kind: str | None = None,
    max_invocations: int | None = None,
    max_invocation_exceptions: int | None = None,
    additional_properties: dict[str, Any] | None = None,
    func: Callable[..., Any] | None = None,
    input_model: type[BaseModel] | Mapping[str, Any] | None = None,
    result_parser: Callable[[Any], str | list[Content]] | _SkipParsingSentinel | None = None,
    **kwargs: Any,
) -> None

FunctionTool.invoke(
    self,
    *,
    arguments: BaseModel | Mapping[str, Any] | None = None,
    context: FunctionInvocationContext | None = None,
    tool_call_id: str | None = None,
    skip_parsing: bool = False,
    **kwargs: Any,
) -> list[Content] | Any

FunctionTool.to_dict(self, *, exclude: set[str] | None = None, exclude_none: bool = True) -> dict[str, Any]
FunctionTool.__call__(self, *args: Any, **kwargs: Any) -> Any
```

A probe of `@tool def add(...)` confirmed `type(add)` is `agent_framework._tools.FunctionTool`, `add.to_dict()` returns `{'type': 'function_tool', 'name': 'add', 'description': 'Add two integers.', 'approval_mode': 'never_require', ... 'input_model': {'properties': ...}}`, and `add(4, b=5)` directly calls the wrapped function. `invoke(...)` is awaitable in practice for normalized framework invocation.

When to use: use `FunctionTool` when you need explicit metadata/schema, declaration-only tools, approval settings, or direct invocation/testing. When not to use: prefer `@tool` for simple implemented Python functions.

Minimal example: `backend/examples/ch05/tools_function_calling.py`.

## Passing tools to `Agent` and chat clients

Implements concept: making tools available to the model and letting the framework execute requested function calls.

Real signatures:

```python
Agent(..., tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None = None, ...)
Agent.run(..., tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None = None, ...)

ChatOptions keys include:
tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None
tool_choice: ToolMode | Literal["auto", "required", "none"]
allow_multiple_tool_calls: bool
```

Tools can be attached at construction (`Agent(..., tools=[...])`) or supplied for a single run (`agent.run(..., tools=[...])`). Concrete public chat clients such as `OpenAIChatClient` include function invocation support; raw clients explicitly warn that they do not include the function-invocation loop.

When to use: attach stable tools to the agent constructor and per-task tools to `run`. When not to use: avoid passing tools to raw clients expecting automatic invocation unless you have composed the invocation layer yourself.

Minimal example: `backend/examples/ch05/tools_function_calling.py`.

## `normalize_tools`, `validate_tools`, `ToolMode`, and invocation configuration / `agent_framework`

Implements concept: framework normalization, validation, and policy controls for tool availability and execution loops.

Real signatures:

```python
normalize_tools(tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None) -> list[ToolTypes]
validate_tools(tools: ToolTypes | Callable[..., Any] | Sequence[ToolTypes | Callable[..., Any]] | None) -> list[ToolTypes]

ToolMode = TypedDict with fields:
mode: Literal["auto", "required", "none"]
required_function_name: str
allowed_tools: list[str]

FunctionInvocationConfiguration = TypedDict with keys including:
enabled, max_iterations, max_function_calls, max_consecutive_errors_per_request,
terminate_on_unknown_calls, additional_tools, include_detailed_errors
```

`normalize_tools` converts callables to `FunctionTool` objects and preserves existing tool objects. `validate_tools` also expands MCP tools where applicable; despite the inspected annotation, a local probe showed it returns a coroutine and should be awaited. `ToolMode` configures whether tools are automatic, required, or disabled and can constrain names. `FunctionInvocationConfiguration` controls the tool execution loop, including max LLM iterations and max total function calls.

When to use: use these for advanced control, test assertions, or middleware/provider code. When not to use: simple agents can pass decorated functions directly.

Minimal example: `backend/examples/ch05/tools_function_calling.py`.

## `FunctionInvocationContext` and tool approvals / `agent_framework.FunctionInvocationContext`, `ToolApprovalMiddleware`

Implements concept: per-tool-call middleware context and optional human/standing approval policy.

Real signatures:

```python
FunctionInvocationContext(
    function: FunctionTool,
    arguments: BaseModel | Mapping[str, Any],
    session: AgentSession | None = None,
    metadata: Mapping[str, Any] | None = None,
    result: Any = None,
    kwargs: Mapping[str, Any] | None = None,
    tools: list[ToolTypes] | None = None,
) -> None

create_always_approve_tool_response(request: Content, *, reason: str | None = None) -> Content
```

`FunctionInvocationContext` is passed through function middleware and exposes the function, validated arguments, optional session, result override, runtime kwargs, and mutable live tool list for progressive tool exposure. Approval helpers and `ToolApprovalMiddleware` exist, but the approval middleware docstring marks it experimental.

When to use: use function middleware context for cross-cutting concerns such as logging, authorization, progressive tools, and custom error handling. When not to use: do not depend on experimental approval APIs for stable public contracts without version pinning.

Minimal example: `backend/examples/ch05/tools_function_calling.py` focuses on stable `tool`/`FunctionTool` usage.
