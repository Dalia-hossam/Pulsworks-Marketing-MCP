from db.models import get_all_campaigns, get_campaign_by_id
from server.validation import validate_campaign_input
from server.auth import is_admin


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