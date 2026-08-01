"""
Complete Demo script asserting all protocol concerns.
"""
from db.database import initialize_database
from client.client import MCPClient
from client.agent import MarketingAgent


def main():
    print("0. Initializing database schema and seed data...")
    initialize_database()

    print("\n1. Capability Negotiation (Client with full capabilities)")
    client = MCPClient("AdminConsoleClient", capabilities={"elicitation": True, "sampling": True})
    client.connect()
    agent = MarketingAgent(client)

    print("\n2. RAG Knowledge Base Tool Call (Option A)")
    agent.execute_task("search_knowledge_base", {"query": "revenue conversions", "campaign_id": 1})

    print("\n3. Dynamic Tool List Changed Notification")
    # Switch session from ANALYST to MANAGER
    client.switch_user_role(2, "manager", "MANAGER")

    print("\n4. Elicitation & Progress Tracking (> $10k budget update)")
    agent.execute_task("update_campaign_budget", {"campaign_id": 1, "new_budget": 15000.0})

    print("\n5. Resource Reading (Policy)")
    policy = agent.read_policy("policy://campaign-rules")
    print(f"Policy fetch preview: {policy[:80]}...")

    print("\n6. Fallback Behavior (Client WITHOUT elicitation capability)")
    legacy_client = MCPClient("LegacyClient", capabilities={"elicitation": False})
    legacy_client.connect()
    legacy_agent = MarketingAgent(legacy_client)
    
    # Attempt high-budget update with legacy client
    legacy_agent.execute_task("update_campaign_budget", {"campaign_id": 1, "new_budget": 20000.0})


if __name__ == "__main__":
    main()