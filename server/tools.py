from db.models import get_all_campaigns, get_campaign_by_id
from server.validation import validate_campaign_input
from server.auth import is_admin
import time

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


def approve_campaign(user, campaign_id: int):
    if not is_admin(user):
        raise PermissionError("Only admins can approve campaigns.")

    return {
        "message": f"Campaign {campaign_id} approved successfully."
    }
    
current_role = "employee"

def change_role(role: str):
    global current_role

    allowed_roles = ["employee", "manager", "admin"]

    if role not in allowed_roles:
        raise ValueError("Invalid role.")

    current_role = role

    return {
        "message": f"Role changed to {role}.",
        "available_tools": (
            ["list_campaigns", "campaign_details"]
            if role != "admin"
            else [
                "list_campaigns",
                "campaign_details",
                "approve_campaign_tool"
            ]
        )
    }


def generate_campaign_report():
    progress = []

    for i in range(5):
        time.sleep(1)
        progress.append(f"{(i + 1) * 20}% completed")

    return {
        "status": "Completed",
        "progress": progress,
        "report": {
            "total_campaigns": 2,
            "active_campaigns": 1,
            "planned_campaigns": 1
        }
    }