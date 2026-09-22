# ADR 001: Use Native LLM Tool Calling

## Status

Accepted

## Context

The agent needs to select and execute application tools such as a calculator,
document lookup, and database query.

An initial implementation used a custom JSON format where the model was asked
to manually produce a tool name and arguments.

This approach introduced parsing problems because the model could return
normal text instead of the expected JSON structure.

The LLM provider supports native tool calling through the OpenAI-compatible
API.

## Decision

Use native LLM tool calling for the agent.

The application provides structured function definitions to the model and
processes the tool calls returned by the model.

Pydantic schemas are then used to validate the arguments before tool
execution.

## Alternatives Considered

### Custom JSON Tool Calling

The model would be instructed to generate a custom JSON object describing the
tool call.

Rejected because:

- Output parsing is more fragile.
- The model may produce text instead of the expected JSON.
- Additional parsing logic is required.

### Agent Framework

A framework such as LangChain or LangGraph could manage the tool-calling
workflow.

Not selected for this implementation because the Day 2 objective is to
understand the core agent loop directly.

A framework can be introduced later if the project requires more complex
state management or orchestration.

## Consequences

### Positive

- Structured tool calls
- Less custom output parsing
- Clear separation between LLM decisions and Python tool execution
- Easier argument validation
- Direct understanding of the underlying agent loop

### Negative

- The application must implement the agent loop itself.
- Provider-specific behavior may need consideration.
- More orchestration code is maintained by the project.

## Result

The agent uses native tool calling while keeping the orchestration logic in
`src/agent_core/agent.py`.