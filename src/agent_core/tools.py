"""
Tools available to the agent.

This module contains the tool implementations, tool registry,
and Pydantic-based argument validation.
"""

from typing import Any

from pydantic import ValidationError

from .schemas import (
    CalculatorArgs,
    DocumentLookupArgs,
    MockDBArgs,
)

# -------------------------------------------------------------------
# Calculator tool
# -------------------------------------------------------------------


def calculator(expression: str) -> float:
    """
    Calculate a basic mathematical expression.

    Only numbers, arithmetic operators, parentheses, decimal points,
    and spaces are allowed.

    Args:
        expression: Mathematical expression such as "25 * 47".

    Returns:
        The calculated numeric result.

    Raises:
        ValueError: If unsupported characters are present.
    """

    allowed_chars = "0123456789+-*/(). "

    if not all(char in allowed_chars for char in expression):
        raise ValueError("Expression contains unsupported characters.")

    return eval(
        expression,
        {"__builtins__": {}},
        {},
    )


# -------------------------------------------------------------------
# Document lookup tool
# -------------------------------------------------------------------

DOCUMENTS = {
    "docuchat": """
    DocuChat is a RAG-powered chat application.
    It uses PostgreSQL with pgvector to store document embeddings.
    Relevant document chunks are retrieved using semantic similarity.
    """,
    "rag": """
    Retrieval-Augmented Generation combines document retrieval
    with language model generation. Relevant context is retrieved
    before the answer is generated.
    """,
    "agents": """
    An AI agent can decide which action to take, use tools,
    observe results, and continue until the task is complete.
    """,
}


def document_lookup(query: str) -> str:
    """
    Search the mock document knowledge base.

    The current implementation performs a simple keyword-based
    lookup against the document names.

    Args:
        query: Search query provided by the agent.

    Returns:
        Matching document content, or a message if no document
        matches the query.
    """

    query_lower = query.lower()
    matches = []

    for name, content in DOCUMENTS.items():
        if name in query_lower:
            matches.append(content.strip())

    if not matches:
        return "No relevant document found."

    return "\n\n".join(matches)


# -------------------------------------------------------------------
# Mock database tool
# -------------------------------------------------------------------

MOCK_DB = {
    "users": [
        {
            "id": 1,
            "name": "Arun",
            "email": "arun@example.com",
        },
        {
            "id": 2,
            "name": "Raj",
            "email": "raj@example.com",
        },
    ],
    "documents": [
        {
            "id": 1,
            "filename": "docuchat.txt",
            "chunks": 5,
        },
        {
            "id": 2,
            "filename": "rag_notes.txt",
            "chunks": 8,
        },
    ],
}


def mock_db_query(
    table: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """
    Query the mock database.

    Args:
        table: Name of the mock database table.
        limit: Maximum number of rows to return.

    Returns:
        A list containing the requested rows.

    Raises:
        ValueError: If the requested table does not exist.
    """

    if table not in MOCK_DB:
        raise ValueError(f"Unknown table: {table}")

    return MOCK_DB[table][:limit]


# -------------------------------------------------------------------
# Tool registry
# -------------------------------------------------------------------

TOOLS = {
    "calculator": {
        "description": "Calculate a mathematical expression.",
        "args_model": CalculatorArgs,
        "function": calculator,
    },
    "document_lookup": {
        "description": "Search the document knowledge base.",
        "args_model": DocumentLookupArgs,
        "function": document_lookup,
    },
    "mock_db_query": {
        "description": "Query the mock database.",
        "args_model": MockDBArgs,
        "function": mock_db_query,
    },
}


# -------------------------------------------------------------------
# Generic tool executor
# -------------------------------------------------------------------


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> Any:
    """
    Validate arguments and execute a registered tool.

    Args:
        tool_name: Name of the tool to execute.
        arguments: Arguments supplied to the tool.

    Returns:
        The result returned by the tool.

    Raises:
        ValueError: If the tool does not exist.
        ValidationError: If the arguments fail Pydantic validation.
    """

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    tool = TOOLS[tool_name]

    args_model = tool["args_model"]
    function = tool["function"]

    validated_args = args_model.model_validate(arguments)

    return function(**validated_args.model_dump())


# -------------------------------------------------------------------
# Safe tool execution with retry
# -------------------------------------------------------------------

MAX_RETRIES = 2


def safe_execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute a tool with validation, retry handling, and
    graceful error reporting.

    Args:
        tool_name: Name of the tool to execute.
        arguments: Tool arguments.

    Returns:
        Dictionary containing either a successful result or
        an error message.
    """

    import time

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        print("\n[Tool Attempt]")
        print(f"{tool_name} - attempt {attempt}")

        try:
            result = execute_tool(
                tool_name,
                arguments,
            )

            return {
                "success": True,
                "result": result,
            }

        except ValidationError as exc:

            return {
                "success": False,
                "error": ("Argument validation failed: " f"{exc}"),
            }

        except Exception as exc:  # noqa: BLE001

            last_error = str(exc)

            print("\n[Tool Error]")
            print(last_error)

            if attempt < MAX_RETRIES:
                time.sleep(0.5)

    return {
        "success": False,
        "error": last_error,
    }
