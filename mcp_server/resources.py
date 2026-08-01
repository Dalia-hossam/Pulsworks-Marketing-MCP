"""
MCP Resource provider for static domain documents.
"""
from pathlib import Path

POLICY_PATH = Path(__file__).parent.parent / "docs" / "Campaign_policy.md"


def list_resources() -> list[dict]:
    return [
        {
            "uri": "policy://campaign-rules",
            "name": "Corporate Campaign & Budget Guidelines",
            "description": "Rules governing campaign spend, human signoff thresholds, and compliance.",
            "mimeType": "text/markdown"
        }
    ]


def read_resource(uri: str) -> str:
    if uri == "policy://campaign-rules":
        if POLICY_PATH.exists():
            return POLICY_PATH.read_text(encoding="utf-8")
        return "# Campaign Policy\nStandard operational policy document."
    raise ValueError(f"Resource not found: {uri}")