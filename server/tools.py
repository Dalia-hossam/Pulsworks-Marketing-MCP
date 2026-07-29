from db.models import (
    get_all_campaigns,
    get_campaign_by_id
)
from server.validation import validate_campaign_input


def list_campaigns():
    campaigns = get_all_campaigns()
    return [dict(campaign) for campaign in campaigns]


def campaign_details(campaign_id):
    valid, error = validate_campaign_input(
        {"campaign_id": campaign_id}
    )

    if not valid:
        return {"error": error}

    campaign = get_campaign_by_id(campaign_id)

    if campaign is None:
        return {"error": "Campaign not found"}

    return dict(campaign)