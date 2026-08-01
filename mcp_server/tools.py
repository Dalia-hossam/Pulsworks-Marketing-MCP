"""
MCP Tool Specifications and Handlers.
"""
import time
from db.database import get_connection
from db.models import get_campaign_by_id
from mcp_server.auth import session
from mcp_server.validation import (
    SearchKnowledgeBaseInput,
    UpdateCampaignBudgetInput,
    PauseCampaignInput
)


def get_available_tools() -> list[dict]:
    """Returns accessible tools based on the active session role."""
    tools = [
        {
            "name": "search_knowledge_base",
            "description": "Search campaign performance notes using BM25 keyword matching.",
            "inputSchema": SearchKnowledgeBaseInput.model_json_schema()
        }
    ]

    # Managers and Admins get write/mutating capabilities
    if session.role in ("MANAGER", "ADMIN"):
        tools.append({
            "name": "update_campaign_budget",
            "description": "Update campaign total budget. Budgets > $10,000 require human sign-off via elicitation.",
            "inputSchema": UpdateCampaignBudgetInput.model_json_schema()
        })
        tools.append({
            "name": "pause_campaign",
            "description": "Pause an active campaign immediately and log audit record.",
            "inputSchema": PauseCampaignInput.model_json_schema()
        })

    return tools


def handle_tool_call(name: str, args: dict, progress_cb=None, elicitation_cb=None) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if name == "update_campaign_budget":
            parsed = UpdateCampaignBudgetInput.model_validate(args)
            campaign = get_campaign_by_id(parsed.campaign_id)
            if not campaign:
                return f"Error: Campaign ID {parsed.campaign_id} not found."

            # Protocol Concern: Elicitation for high-budget updates (> $10k)
            if parsed.new_budget > 10000.0:
                if not session.supports_elicitation:
                    return (
                        "ERROR: Budget update exceeds $10,000 threshold, which requires human sign-off. "
                        "The connected client does not support elicitation capabilities."
                    )
                
                # Stop mid-call and elicit human sign-off
                approved = elicitation_cb(
                    f"RISK CONFIRMATION: Requested budget update for Campaign #{parsed.campaign_id} "
                    f"is ${parsed.new_budget:,.2f} (exceeds $10,000 limit). Do you approve this increase?"
                )
                if not approved:
                    return "OPERATION CANCELLED: Human operator rejected budget increase."

            # Protocol Concern: Progress Tracking for batch execution
            if progress_cb:
                progress_cb(20, "Validating campaign status...")
                time.sleep(0.3)
                progress_cb(60, "Updating database budget allocation...")
                time.sleep(0.3)

            cursor.execute("UPDATE campaigns SET budget = ? WHERE id = ?", (parsed.new_budget, parsed.campaign_id))
            cursor.execute(
                "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                (session.user_id, "UPDATE_BUDGET", f"Campaign {parsed.campaign_id} budget updated to ${parsed.new_budget}")
            )
            conn.commit()

            if progress_cb:
                progress_cb(100, "Budget update completed successfully.")

            return f"Successfully updated Campaign #{parsed.campaign_id} budget to ${parsed.new_budget:,.2f}."

        elif name == "pause_campaign":
            parsed = PauseCampaignInput.model_validate(args)
            cursor.execute("UPDATE campaigns SET status = 'PAUSED' WHERE id = ?", (parsed.campaign_id,))
            cursor.execute(
                "INSERT INTO audit_logs (user_id, action, details) VALUES (?, ?, ?)",
                (session.user_id, "PAUSE_CAMPAIGN", f"Campaign {parsed.campaign_id} paused. Reason: {parsed.reason}")
            )
            conn.commit()
            return f"Campaign #{parsed.campaign_id} is now PAUSED. Audit record logged."

    finally:
        conn.close()

    raise ValueError(f"Unknown or unauthorized tool call: {name}")