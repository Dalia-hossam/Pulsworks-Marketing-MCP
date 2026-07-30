from pathlib import Path

RESOURCE_PATH = Path(__file__).parent.parent / "docs" / "campaign_policy.md"


def get_campaign_policy() -> str:
    """Reads and returns the read-only marketing campaign compliance policy document."""
    if not RESOURCE_PATH.exists():
        # Fallback content if file path is missing
        return """# Marketing Campaign Policy (Fallback)
1. All budget increases above 25% require manager approval.
2. High-risk campaigns must be reviewed by compliance.
"""
    
    with open(RESOURCE_PATH, "r", encoding="utf-8") as file:
        return file.read()