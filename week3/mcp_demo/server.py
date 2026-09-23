from mcp.server import MCPServer


mcp = MCPServer(
    "Learning MCP Server",
    instructions="A simple MCP learning server with two tools and one resource.",
)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def calculate_rectangle_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width


@mcp.resource("info://project")
def project_info() -> str:
    """Return information about the AI learning project."""
    return (
        "This MCP server is part of the AI learning project. "
        "It demonstrates MCP tools and resources."
    )


if __name__ == "__main__":
    mcp.run()