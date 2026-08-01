"""
MCP Canned Prompt Templates.
"""

def list_prompts() -> list[dict]:
    return [
        {
            "name": "pause_campaign_explanation",
            "description": "Template to draft an executive brief when pausing an underperforming campaign",
            "arguments": [
                {"name": "campaign_id", "description": "ID of campaign", "required": True},
                {"name": "reason", "description": "Reason for pausing", "required": True}
            ]
        }
    ]


def get_prompt(name: str, args: dict) -> str:
    if name == "pause_campaign_explanation":
        c_id = args.get("campaign_id", "")
        reason = args.get("reason", "")
        return (
            f"Draft an official email notification for Campaign #{c_id}.\n"
            f"Explain to the account manager that the campaign has been paused due to: '{reason}'.\n"
            f"Provide 2-3 recommended next steps based on campaign policies."
        )
    raise ValueError(f"Prompt template not found: {name}")