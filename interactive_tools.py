"""
Interactive Tool Executor & Gemini AI Assistant
Run: python interactive_tools.py
"""
import json
from db.database import initialize_database
from mcp_server.rag.rag_tool import index_campaign_data
from client.client import MCPClient
from client.agent import MarketingAgent


def main():
    print("⚡ Initializing Database & MCP Server...")
    initialize_database()
    index_campaign_data()

    client = MCPClient("InteractiveUserClient")
    client.connect()
    
    # Authenticate as Manager to unlock all tools
    client.switch_user_role(user_id=2, username="manager", new_role="MANAGER")
    agent = MarketingAgent(client)

    last_tool_result = None

    while True:
        tools = client.list_tools()
        print("\n================ AVAILABLE MCP TOOLS ================")
        for idx, tool in enumerate(tools, 1):
            print(f" [{idx}] {tool['name']} - {tool.get('description', '')}")
        
        print("\n================ OTHER ACTIONS ================")
        print(" [R] Read Policy Resource (policy://campaign-rules)")
        print(" [A] Ask Gemini AI (Analyze last tool result or custom query)")
        print(" [Q] Quit")
        print("=====================================================")

        choice = input("\nSelect an option: ").strip()

        if choice.upper() == 'Q':
            print("Exiting interactive menu. Goodbye!")
            break

        elif choice.upper() == 'R':
            last_tool_result = agent.read_policy("policy://campaign-rules")

        elif choice.upper() == 'A':
            if last_tool_result:
                print(f"\n💡 Current Tool Context:\n{last_tool_result}\n")
            
            user_prompt = input("Enter your prompt for Gemini AI: ").strip()
            
            full_prompt = f"""
            Retrieved Context:
            {last_tool_result if last_tool_result else 'No prior tool output context.'}

            User Question:
            {user_prompt}
            """
            print("\n🤖 Querying Gemini...")
            response = agent.ask_gemini(full_prompt)
            print("\n================ GEMINI RESPONSE ================")
            print(response)
            print("==================================================")

        elif choice.isdigit() and 1 <= int(choice) <= len(tools):
            selected_tool = tools[int(choice) - 1]
            tool_name = selected_tool["name"]
            
            print(f"\n🛠️ Selected Tool: {tool_name}")
            schema = selected_tool.get("inputSchema", {}).get("properties", {})
            print(f"Required Arguments: {list(schema.keys())}")
            
            args = {}
            for key, prop in schema.items():
                val_type = prop.get("type", "string")
                raw_val = input(f" Enter value for '{key}' ({val_type}): ").strip()
                
                # Basic type conversions
                if val_type == "integer":
                    args[key] = int(raw_val)
                elif val_type == "number":
                    args[key] = float(raw_val)
                elif val_type == "boolean":
                    args[key] = raw_val.lower() in ("true", "1", "yes")
                else:
                    args[key] = raw_val

            print(f"\nExecuting '{tool_name}' with args {args}...")
            last_tool_result = agent.execute_task(tool_name, args)

        else:
            print("❌ Invalid selection. Please try again.")


if __name__ == "__main__":
    main()