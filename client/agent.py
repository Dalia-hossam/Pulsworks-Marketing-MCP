import asyncio
import json
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def run_interactive_agent():
    print("=" * 60)
    print("🤖 INTERACTIVE LOCAL MCP AGENT")
    print("=" * 60)

    # 1. Connect to MCP Server via stdio
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 2. Perform MCP Handshake
            await session.initialize()
            print("[✓] Connected to MCP Server successfully.\n")

            # 3. Discover available tools on the server
            tools_response = await session.list_tools()
            available_tools = [tool.name for tool in tools_response.tools]
            print(f"🛠️ Available Tools on Server: {available_tools}\n")

            # 4. Interactive Loop for User Prompts
            while True:
                user_prompt = input("\n💬 Enter your Prompt (or type 'exit' to quit): ").strip()
                
                if not user_prompt:
                    continue
                if user_prompt.lower() in ["exit", "quit", "q"]:
                    print("👋 Exiting Agent. Goodbye!")
                    break

                print(f"\n🧠 Agent processing prompt: '{user_prompt}'...")
                prompt_lower = user_prompt.lower()

                # Dynamic Tool Intent Matching adjusted for RAG & policies
                if any(keyword in prompt_lower for keyword in ["search", "policy", "guidelines", "discount", "budget", "rule", "approval"]):
                    selected_tool = "search_knowledge_base"
                    tool_args = {
                        "query": user_prompt,
                        "entity_id": "campaign_1",
                        "top_k": 3
                    }
                elif "report" in prompt_lower or "summary" in prompt_lower or "analytics" in prompt_lower:
                    selected_tool = "campaign_report"
                    tool_args = {}
                elif "approve campaign" in prompt_lower or "execute approval" in prompt_lower:
                    selected_tool = "approve_campaign_tool"
                    tool_args = {"campaign_id": 1, "username": "admin", "password": "admin123"}
                elif "role" in prompt_lower or "admin" in prompt_lower:
                    selected_tool = "set_role"
                    tool_args = {"role": "ADMIN"}
                elif "detail" in prompt_lower or "get" in prompt_lower:
                    selected_tool = "campaign_details"
                    tool_args = {"campaign_id": 1}
                else:
                    selected_tool = "list_campaigns"
                    tool_args = {}

                print(f"⚙️  Agent Intent Match -> Tool: '{selected_tool}' | Args: {tool_args}")

                # 5. Execute Tool via MCP Session
                try:
                    result = await session.call_tool(selected_tool, arguments=tool_args)
                    result_content = result.content[0].text if result.content else "{}"
                    
                    print("\n🎯 MCP Server Response:")
                    print(result_content)
                except Exception as e:
                    print(f"❌ Error executing tool: {e}")


if __name__ == "__main__":
    asyncio.run(run_interactive_agent())