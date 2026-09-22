"""
Core agent loop using native LLM tool calling.

The agent follows the basic cycle:

LLM -> Tool Call -> Validation -> Tool Execution
    -> Observation -> LLM -> Final Answer
"""

import json
import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from .tools import safe_execute_tool

load_dotenv()
MODEL = "openai/gpt-oss-20b"
MAX_RETRIES = 2
MAX_STEPS = 8
TIMEOUT_SECONDS = 60


SYSTEM_PROMPT = """
You are a simple tool-using AI agent.

Your job is to solve the user's request using the available tools.

Available tools:
- calculator
- document_lookup
- mock_db_query

Use a tool when it is necessary.
After receiving a tool result, continue solving the user's original request.

Do not invent tool results.
Do not invent tools.
If the task can be answered without a tool, answer directly.
"""


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate",
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "document_lookup",
            "description": "Search the document knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for the document knowledge base",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mock_db_query",
            "description": "Query the mock database for structured records.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table": {
                        "type": "string",
                        "description": "Name of the database table to query",
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 20,
                        "description": "Maximum number of rows to return",
                    },
                },
                "required": ["table", "limit"],
                "additionalProperties": False,
            },
        },
    },
]


def create_client() -> OpenAI:
    """
    Create the OpenAI-compatible Groq client.

    Returns:
        Configured OpenAI client.

    Raises:
        ValueError: If OPENAI_API_KEY is not configured.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )


def log_event(event_type: str, content: Any) -> None:
    """
    Print a structured agent event.

    Args:
        event_type: Type of event being logged.
        content: Event information.
    """

    print(f"\n[{event_type}]")
    print(content)


def ask_agent(
    client: OpenAI,
    messages: list[dict[str, Any]],
):
    """
    Send the current conversation to the LLM.

    Args:
        client: Configured OpenAI-compatible client.
        messages: Current agent conversation.

    Returns:
        LLM response.
    """

    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        reasoning_effort="low",
        tools=TOOL_SCHEMAS,
        tool_choice="auto",
    )


def run_agent(user_request: str) -> str:
    """
    Run the complete agent loop.

    The loop repeatedly asks the LLM what to do, executes requested
    tools, records observations, and continues until a final answer
    is produced or a safety limit is reached.

    Args:
        user_request: User's original request.

    Returns:
        Final agent response or a graceful stop message.
    """

    start_time = time.time()
    client = create_client()

    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_request,
        },
    ]

    for step in range(1, MAX_STEPS + 1):

        log_event("Step", step)

        # -----------------------------------------------------------
        # Timeout protection
        # -----------------------------------------------------------

        if time.time() - start_time >= TIMEOUT_SECONDS:
            log_event("Stop", "Timeout reached.")
            return "Agent stopped because the timeout was reached."

        # -----------------------------------------------------------
        # Ask the LLM
        # -----------------------------------------------------------

        try:
            response = ask_agent(
                client,
                messages,
            )

        except Exception as exc:  # noqa: BLE001
            log_event("LLM Error", str(exc))
            return "Agent stopped because the LLM request failed."

        message = response.choices[0].message

        # -----------------------------------------------------------
        # Final answer
        # -----------------------------------------------------------

        if not message.tool_calls:

            final_answer = message.content or "No final answer provided."

            log_event(
                "Final",
                final_answer,
            )

            return final_answer

        # -----------------------------------------------------------
        # Process tool call
        # -----------------------------------------------------------

        tool_call = message.tool_calls[0]

        tool_name = tool_call.function.name

        try:
            arguments = json.loads(tool_call.function.arguments)

        except json.JSONDecodeError:
            log_event(
                "Tool Error",
                "Invalid tool arguments.",
            )

            return "Agent stopped because the tool " "arguments were invalid."

        # -----------------------------------------------------------
        # Thought
        # -----------------------------------------------------------

        log_event(
            "Thought",
            f"Agent decided to use the '{tool_name}' tool.",
        )

        # -----------------------------------------------------------
        # Action
        # -----------------------------------------------------------

        log_event(
            "Action",
            {
                "tool": tool_name,
                "arguments": arguments,
            },
        )

        # -----------------------------------------------------------
        # Execute tool
        # -----------------------------------------------------------

        tool_result = safe_execute_tool(
            tool_name,
            arguments,
        )

        # -----------------------------------------------------------
        # Observation
        # -----------------------------------------------------------

        log_event(
            "Observation",
            tool_result,
        )

        # Add assistant tool-call message
        messages.append(message)

        # Add tool result to conversation
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result,
                    default=str,
                ),
            }
        )

    log_event(
        "Stop",
        "Maximum number of steps reached.",
    )

    return "Agent stopped because the maximum number " "of steps was reached."
