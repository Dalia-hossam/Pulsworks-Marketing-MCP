import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():
    server = StdioServerParameters(
        command="python",
        args=["-m", "server.server"],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("Available Tools:\n")

            for tool in tools.tools:
                print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())