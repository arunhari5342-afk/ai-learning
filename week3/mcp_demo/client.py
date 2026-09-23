import asyncio

from mcp import Client, StdioServerParameters


async def main() -> None:
    server_params = StdioServerParameters(
        command="python",
        args=["week3/mcp_demo/server.py"],
    )

    async with Client(server_params) as client:

        print("=" * 60)
        print("CONNECTED TO MCP SERVER")
        print("=" * 60)

        print("\nServer information:")
        print(client.server_info)

        print("\nProtocol version:")
        print(client.protocol_version)

        print("\nServer capabilities:")
        print(client.server_capabilities)

        # --------------------------------------------------
        # 1. Discover tools
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("DISCOVERING TOOLS")
        print("=" * 60)

        tools_result = await client.list_tools()

        for tool in tools_result.tools:
            print(f"\nTool: {tool.name}")
            print(f"Description: {tool.description}")
            print(f"Input schema: {tool.input_schema}")

        # --------------------------------------------------
        # 2. Invoke add tool
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("CALLING add")
        print("=" * 60)

        result = await client.call_tool(
            "add",
            {
                "a": 10,
                "b": 5,
            },
        )

        print("Result:")
        print(result)

        # --------------------------------------------------
        # 3. Invoke multiply tool
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("CALLING multiply")
        print("=" * 60)

        result = await client.call_tool(
            "multiply",
            {
                "a": 6,
                "b": 7,
            },
        )

        print("Result:")
        print(result)


        print("\n" + "=" * 60)
        print("CALLING calculate_rectangle_area")
        print("=" * 60)

        result = await client.call_tool(
            "calculate_rectangle_area",
    {
               "length": 10,
               "width": 5,
    },
)

        print("Result:")
        print(result)

        # --------------------------------------------------
        # 4. Discover resources
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("DISCOVERING RESOURCES")
        print("=" * 60)

        resources_result = await client.list_resources()

        for resource in resources_result.resources:
            print(f"\nResource URI: {resource.uri}")
            print(f"Name: {resource.name}")

        # --------------------------------------------------
        # 5. Read resource
        # --------------------------------------------------

        print("\n" + "=" * 60)
        print("READING PROJECT RESOURCE")
        print("=" * 60)

        resource_result = await client.read_resource(
            "info://project"
        )

        print(resource_result)


if __name__ == "__main__":
    asyncio.run(main())