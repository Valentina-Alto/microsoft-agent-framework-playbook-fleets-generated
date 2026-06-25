# Chapter 1 theory brief: What is an agent?

Artifact path: `content/research/01-theory.md`

## Concepts covered

- What an AI agent is
- Agent vs. chatbot
- Agent vs. deterministic workflow/automation
- Core agent loop: perceive, reason, act
- Tool use
- Autonomy and goal-directedness
- When agents are the right tool
- When agents are NOT the right tool
- MAF vocabulary: agent, instructions, chat client, tools, workflow, orchestration, multi-agent

## What an AI agent is

An AI agent is an application that uses a model to reason about a request and take actions toward a goal, usually by combining model reasoning, instructions, and tools. Microsoft Foundry describes an agent as an AI application that reasons over user requests and can take autonomous actions, and Microsoft Agent Framework (MAF) describes agents as LLM-backed components that process inputs, call tools or MCP servers, and generate responses. Sources: https://learn.microsoft.com/en-us/azure/foundry/agents/overview, https://learn.microsoft.com/en-us/agent-framework/overview/

- **Problem it solves:** Agents are useful when the application must decide how to proceed from context rather than follow one fixed path every time.
- **Key distinctions:** An agent is not just "a model call"; it is the model plus behavior constraints, available tools, and runtime support for multi-step interaction.
- **Common misconceptions:** "Agent" does not automatically mean fully independent, safe, or correct; Microsoft explicitly says builders are responsible for testing, responsible AI mitigations, and safety decisions for their use case. Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **Implemented in MAF by:** `Agent` + `instructions` + chat client boundary — Chapter 3; chat clients/providers — Chapter 4; tools — Chapter 5.

## Agent vs. chatbot

A chatbot is typically a conversational interface that returns text, while an agent can also call tools, access external data, and make multi-step decisions to complete a task. Microsoft Foundry states that, unlike a simple chatbot that only generates text, an agent can call tools, access external data, and sometimes operate without a chat interface in the background. Source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

- **Problem it solves:** The agent framing helps developers design beyond "answer a message" toward "complete a task with controlled capabilities."
- **Key distinctions:** Chat is an interface; agency is a task-solving pattern. An agent can be conversational, but a conversational UI alone does not make something an agent.
- **Common misconceptions:** If an app has a chat box, it is not necessarily agentic; if an app has no chat UI, it can still be an agent when it reasons and acts on a user's or organization's behalf.
- **Implemented in MAF by:** Agent invocation and instructions — Chapter 3; messages, conversations, and session state — Chapter 4.

## Agent vs. deterministic workflow/automation

A deterministic workflow is a predefined sequence or graph of operations, while an agent's steps are dynamic and model-driven based on context and available tools. Microsoft Learn distinguishes agents from workflows by saying agent steps are determined by the LLM, whereas workflow flow is explicitly defined for more control over the execution path. Source: https://learn.microsoft.com/en-us/agent-framework/workflows/

- **Problem it solves:** The distinction prevents teams from using probabilistic planning where ordinary code or a defined process would be simpler, cheaper, and easier to verify.
- **Key distinctions:** Use an agent for open-ended or conversational tasks that need autonomous tool use and planning; use a workflow for well-defined steps, explicit execution order, and coordination among agents or functions. Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **Common misconceptions:** Workflows are not the "less advanced" option; they are the right abstraction when the process path is known and control matters.
- **Implemented in MAF by:** Workflows, `WorkflowBuilder`, executors, edges — Chapter 6; handoff and group chat orchestration — Chapter 7.

## Core agent loop: perceive, reason, act

At the concept level, an agent loop can be described as perceiving input/context, reasoning with a model, and acting through responses or tools. MAF's agent documentation describes a structured runtime model that coordinates user interaction, model inference, and tool execution in a deterministic loop. Source: https://learn.microsoft.com/en-us/agent-framework/agents/

- **Problem it solves:** The loop explains how an agent can move from a user request to one or more model/tool turns instead of only producing a single answer.
- **Key distinctions:** "Deterministic loop" here refers to the framework's runtime structure, not to deterministic model outputs or guaranteed business results.
- **Common misconceptions:** The loop is not permission to let an agent run forever; Microsoft Architecture guidance recommends iteration limits to guard against infinite tool-call loops. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Agent runtime execution — Chapter 3; conversations/sessions — Chapter 4; tools — Chapter 5; workflow events/streaming — Chapter 8.

## Tool use

Tools extend an agent beyond text generation by giving it controlled ways to interact with external systems, execute code, search data, or call MCP servers. MAF documents tool categories including function tools, code interpreter, file search, web search, hosted MCP tools, local MCP tools, and provider-specific tools. Source: https://learn.microsoft.com/en-us/agent-framework/agents/tools/

- **Problem it solves:** Tools let the model ask the application to perform grounded actions, such as looking up current data or invoking domain code, without embedding those capabilities inside the model.
- **Key distinctions:** Tools should be curated capabilities with clear boundaries; tool approval can gate tool invocations through a human-in-the-loop decision before the model receives the result. Source: https://learn.microsoft.com/en-us/agent-framework/agents/tools/
- **Common misconceptions:** More tools are not always better; tool overload can justify splitting work into specialized agents or workflows only when a single agent cannot reliably handle the task. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Function tools, hosted/local MCP tools, provider tools, tool approval — Chapter 5; human-in-the-loop — Chapter 8.

## Autonomy and goal-directedness

Autonomy means the agent has bounded discretion to choose steps toward a goal; it does not mean it operates without constraints. Foundry describes agents as taking autonomous actions to fulfill requests, while also emphasizing instructions, tools, identity, security, content filters, and observability as parts of the platform model. Source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

- **Problem it solves:** Bounded autonomy lets developers handle varied requests without hard-coding every branch, while still constraining what the agent can see and do.
- **Key distinctions:** The goal comes from the user request and instructions; the action space comes from the tools and runtime boundaries.
- **Common misconceptions:** Autonomy is not trust. Microsoft warns that builders must review and test applications in their specific context and implement appropriate quality, reliability, security, and trustworthiness measures. Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **Implemented in MAF by:** Instructions and agent identity — Chapter 3; tools and approvals — Chapter 5; middleware/observability — Chapter 9.

## When agents are the right tool

Agents are a good fit when the task is open-ended or conversational, requires autonomous tool use and planning, and can often be handled by a single LLM-backed agent with tools. MAF's overview explicitly recommends agents for open-ended or conversational tasks, autonomous tool use and planning, or a single LLM call with tools. Source: https://learn.microsoft.com/en-us/agent-framework/overview/

- **Problem it solves:** This gives developers a decision rule before they reach for framework components.
- **Key distinctions:** Start with the lowest complexity that reliably meets the requirement: direct model call, then single agent with tools, then multi-agent orchestration only when needed. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Common misconceptions:** Production readiness is not achieved by choosing an agent framework alone; MAF provides building blocks such as state management, middleware, telemetry, workflows, and provider flexibility, but application-specific safeguards remain the developer's responsibility. Sources: https://learn.microsoft.com/en-us/agent-framework/overview/, https://github.com/microsoft/agent-framework
- **Implemented in MAF by:** Chapter 2 pattern map; single-agent construction — Chapter 3; tools — Chapter 5; observability and middleware — Chapter 9.

## MAF vocabulary: agent

In MAF, an agent is the common abstraction for a component that can be invoked consistently across provider-backed or custom implementations. Microsoft Learn states that Python agents derive from a common `Agent` base class, enabling common higher-level functionality such as multi-agent orchestrations. Source: https://learn.microsoft.com/en-us/agent-framework/agents/

- **Problem it solves:** A common agent abstraction lets the rest of the framework compose agents without depending on one provider's API shape.
- **Key distinctions:** The agent is the behavior boundary; the model provider and chat client are dependencies behind that boundary.
- **Common misconceptions:** The agent abstraction does not imply every provider has identical capabilities; provider support varies for tools, structured outputs, code interpreter, file search, MCP tools, and background responses. Source: https://learn.microsoft.com/en-us/agent-framework/agents/providers/
- **Implemented in MAF by:** `Agent` — Chapter 3; providers/chat clients — Chapter 4.

## MAF vocabulary: instructions

Instructions define the agent's goals, constraints, and behavior. Foundry lists instructions as one of an agent's three core components, alongside model and tools. Source: https://learn.microsoft.com/en-us/azure/foundry/agents/overview

- **Problem it solves:** Instructions make the agent's role and constraints explicit instead of leaving all behavior implicit in user prompts.
- **Key distinctions:** Instructions guide behavior but do not replace programmatic controls such as tool scoping, approval, validation, middleware, or workflow boundaries.
- **Common misconceptions:** Better instructions alone cannot guarantee safe or correct behavior; Microsoft places responsibility on application builders to test and apply mitigations for their specific use cases. Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **Implemented in MAF by:** Agent instructions and identity/name — Chapter 3.

## MAF vocabulary: chat client

A chat client is the model/provider boundary that lets an agent use an inference service. MAF documentation says any inference service that provides a chat client implementation can be used with the standard Python `Agent`, and MAF supports providers such as Microsoft Foundry, Azure OpenAI, OpenAI, Anthropic, Ollama, GitHub Copilot, Copilot Studio, and custom providers. Sources: https://learn.microsoft.com/en-us/agent-framework/agents/, https://learn.microsoft.com/en-us/agent-framework/agents/providers/

- **Problem it solves:** The chat client separates "what the agent does" from "which model service runs inference."
- **Key distinctions:** Provider choice affects available capabilities; the provider matrix shows differences in function tools, structured outputs, code interpreter, file search, MCP tools, and background responses. Source: https://learn.microsoft.com/en-us/agent-framework/agents/providers/
- **Common misconceptions:** Swapping providers is not purely cosmetic; capability, state, tool, and hosting behavior can differ.
- **Implemented in MAF by:** `ChatClient`, `FoundryChatClient`, providers, messages — Chapter 4.

## MAF vocabulary: tools

In MAF, tools are the controlled capabilities an agent can call during conversation or execution. Microsoft Learn says tools allow agents to interact with external systems, execute code, search data, and more. Source: https://learn.microsoft.com/en-us/agent-framework/agents/tools/

- **Problem it solves:** Tools connect model reasoning to application capabilities without asking the model to invent facts or perform side effects directly.
- **Key distinctions:** Local function tools, hosted tools, MCP tools, and provider tools have different execution and approval models.
- **Common misconceptions:** Tools are not automatically safe because the model chose them; tool approval and human-in-the-loop patterns exist because tool actions may need explicit review. Source: https://learn.microsoft.com/en-us/agent-framework/agents/tools/
- **Implemented in MAF by:** Tools/function calling/tool schemas/agent skills — Chapter 5.

## MAF vocabulary: workflow

A workflow is an explicitly defined process that can include agents and functions as components. MAF workflows use graph-based architecture with executors and edges, and Microsoft Learn says workflows are designed for complex business processes with multiple agents, human interactions, and integrations where the flow is explicitly defined. Source: https://learn.microsoft.com/en-us/agent-framework/workflows/

- **Problem it solves:** Workflows add control, validation, routing, streaming, checkpointing, and human interaction around multi-step processes.
- **Key distinctions:** Agents choose dynamic steps through model reasoning; workflows define the execution path through code or graph structure.
- **Common misconceptions:** A workflow may include agents, but the workflow itself is not automatically "more agentic"; it is often the control structure around agentic components.
- **Implemented in MAF by:** Workflows, functional workflow API, `WorkflowBuilder`, executors, edges — Chapter 6; streaming/checkpointing/HITL — Chapter 8.

## MAF vocabulary: orchestration

Orchestration is the coordination layer that decides how agents, tools, functions, and humans are sequenced or combined. MAF workflows support multi-agent orchestration patterns including sequential, concurrent, handoff, and group collaboration; Azure Architecture guidance frames orchestration as useful when multiple specialized agents must coordinate and a single agent is not reliable enough because of prompt complexity, tool overload, or security boundaries. Sources: https://learn.microsoft.com/en-us/agent-framework/workflows/, https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

- **Problem it solves:** Orchestration makes complex agent systems understandable by making coordination explicit.
- **Key distinctions:** Orchestration can be deterministic, such as a sequential workflow, or more collaborative, such as group chat and handoff patterns.
- **Common misconceptions:** Multi-agent orchestration is not the default starting point; it adds coordination overhead, latency, cost, and failure modes. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Sequential/concurrent workflows — Chapter 6; handoff and group chat — Chapter 7.

## MAF vocabulary: multi-agent

A multi-agent system coordinates multiple specialized agents to solve work that is too broad or constrained for a single agent. Azure Architecture guidance says multiagent orchestration is appropriate for cross-domain problems, distinct security boundaries, or tasks that benefit from parallel specialization, but it adds coordination overhead, latency, and failure modes. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

- **Problem it solves:** Multi-agent design lets each agent carry narrower instructions, tools, knowledge, and security boundaries.
- **Key distinctions:** Multiple agents should be justified by specialization, security, parallelism, or complexity—not by novelty.
- **Common misconceptions:** "More agents" is not automatically more capable; Microsoft recommends using the lowest level of complexity that reliably meets requirements. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Implemented in MAF by:** Agent-as-tool composition — Chapter 5; workflow orchestration — Chapter 6; handoff and group chat — Chapter 7.

## When agents are NOT the right tool

- **Use a normal function when deterministic code is enough.** MAF's overview says, "If you can write a function to handle the task, do that instead of using an AI agent." Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **Use a direct model call when there is no agent logic or tool access.** Azure Architecture guidance lists direct model calls as the least complex option for single-pass tasks such as classification, summarization, and translation when prompting is sufficient. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Use a workflow when the process has known steps and control matters.** MAF recommends workflows for well-defined steps, explicit control over execution order, and coordination among multiple agents or functions. Source: https://learn.microsoft.com/en-us/agent-framework/overview/
- **Avoid multi-agent systems until a single agent is insufficient.** Microsoft guidance says multi-agent orchestration adds coordination overhead, latency, cost, and failure modes, so use the lowest complexity that reliably meets the requirement. Source: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Avoid agents where uncontrolled side effects are unacceptable.** Tool approval exists to gate tool invocations through human-in-the-loop review, which implies that side-effecting capabilities should be deliberately scoped and approved. Source: https://learn.microsoft.com/en-us/agent-framework/agents/tools/
- **Avoid treating a framework as a safety guarantee.** Microsoft says application builders remain responsible for reviewing, testing, and applying responsible AI mitigations and trustworthiness measures for their use case. Source: https://learn.microsoft.com/en-us/agent-framework/overview/

## Sources

- https://learn.microsoft.com/en-us/agent-framework/
- https://learn.microsoft.com/en-us/agent-framework/overview/
- https://learn.microsoft.com/en-us/agent-framework/agents/
- https://learn.microsoft.com/en-us/agent-framework/agents/tools/
- https://learn.microsoft.com/en-us/agent-framework/agents/providers/
- https://learn.microsoft.com/en-us/agent-framework/agents/conversations/
- https://learn.microsoft.com/en-us/agent-framework/workflows/
- https://learn.microsoft.com/en-us/agent-framework/workflows/workflows
- https://learn.microsoft.com/en-us/azure/foundry/agents/overview
- https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- https://github.com/microsoft/agent-framework
- https://devblogs.microsoft.com/agent-framework/
