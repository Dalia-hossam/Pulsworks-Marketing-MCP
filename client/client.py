import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def run_client():
    # 1. Define Stdio Server connection parameters
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"],
    )

    print("🔌 Connecting to MCP Server via stdio transport...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 2. Capability Negotiation & Handshake
            init_result = await session.initialize()
            print("✅ Handshake successful!")
            print(f"🖥️  Server Info: {init_result.serverInfo.name} v{init_result.serverInfo.version}")
            
            # Check Server Capabilities explicitly
            capabilities = init_result.capabilities
            print(f"📋 Declared Capabilities: {list(capabilities.__dict__.keys())}\n")

            # 3. Discover Available Tools
            tools_result = await session.list_tools()
            print("🧰 Available Tools:")
            for tool in tools_result.tools:
                print(f"  • {tool.name}: {tool.description}")

            # 4. Discover Available Resources
            resources_result = await session.list_resources()
            print("\n📚 Available Resources:")
            for res in resources_result.resources:
                print(f"  • {res.uri} ({res.name})")

            # 5. Discover Available Prompts
            prompts_result = await session.list_prompts()
            print("\n💬 Available Prompts:")
            for prompt in prompts_result.prompts:
                print(f"  • {prompt.name}: {prompt.description}")

            return session

if __name__ == "__main__":
    asyncio.run(run_client())