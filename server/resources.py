from pathlib import Path

RESOURCE_PATH = Path(__file__).parent.parent / "docs" / "campaign_policy.md"


def get_campaign_policy():
    with open(RESOURCE_PATH, "r", encoding="utf-8") as file:
        return file.read()