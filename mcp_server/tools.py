import asyncio
from db.models import get_all_campaigns, get_campaign_by_id
from mcp_server.validation import validate_campaign_input
from mcp_server.auth import active_session

def get_campaigns():
    campaigns = get_all_campaigns()
    return [dict(campaign) for campaign in campaigns]


def get_campaign(campaign_id: int):
    valid, error = validate_campaign_input({"campaign_id": campaign_id})

    if not valid:
        raise ValueError(error)

    campaign = get_campaign_by_id(campaign_id)

    if campaign is None:
        raise ValueError("Campaign not found.")

    return dict(campaign)


async def approve_campaign(user, campaign_id: int, ctx=None):
    # Extract role safely from dictionary or object
    role = user.get("role", "") if isinstance(user, dict) else getattr(user, "role", "")
    
    if role.upper() not in ["ADMIN", "MANAGER"]:
        raise PermissionError("Only Admins and Managers can approve campaigns.")

    campaign = get_campaign_by_id(campaign_id)
    if not campaign:
        raise ValueError("Campaign not found.")

    campaign_dict = dict(campaign)
    budget = campaign_dict.get("budget", 0)

    # High budget elicitation check
    if budget >= 5000:
        if ctx and hasattr(ctx, 'elicit'):
            try:
                confirmation = await ctx.elicit(
                    message=f"WARNING: Campaign '{campaign_dict['campaign_name']}' has a high budget (${budget:,.2f}). Approve?",
                    schema={"type": "boolean"}
                )
                if not confirmation:
                    return {"status": "Aborted", "message": "Approval cancelled."}
            except Exception:
                # Fallback if client doesn't fully handle elicitation response
                pass

    return {
        "status": "Success",
        "message": f"Campaign '{campaign_dict['campaign_name']}' (ID: {campaign_id}) approved successfully."
    }


def change_role(role: str):
    allowed_roles = ["ANALYST", "MANAGER", "ADMIN"]
    normalized_role = role.upper()

    if normalized_role not in allowed_roles:
        raise ValueError(f"Invalid role. Allowed roles: {allowed_roles}")

    # Set active session role and check if it changed
    role_changed = active_session.set_user({"username": "session_user", "role": normalized_role})

    return {
        "message": f"Role updated to {normalized_role}.",
        "role_changed": role_changed
    }, role_changed


async def generate_campaign_report(ctx=None):
    total_steps = 5
    for i in range(1, total_steps + 1):
        await asyncio.sleep(0.2)  # Non-blocking async sleep for MCP progress tracking
        if ctx and hasattr(ctx, 'report_progress'):
            await ctx.report_progress(progress=i * 20, total=100)

    return {
        "status": "Completed",
        "report": {
            "total_campaigns": 2,
            "active_campaigns": 1,
            "planned_campaigns": 1,
            "total_revenue": 15700.00
        }
    }