from mcp.server.fastmcp import FastMCP

from server.tools import list_campaigns, campaign_details
from server.resources import get_campaign_policy
from server.prompts import generate_campaign_summary_prompt

mcp = FastMCP("PulseWorks Marketing MCP")


@mcp.tool()
def get_campaigns():
    """Return all marketing campaigns."""
    return list_campaigns()


@mcp.tool()
def get_campaign(campaign_id: int):
    """Return details for one campaign."""
    return campaign_details(campaign_id)


@mcp.resource("policy://campaign")
def campaign_policy():
    return get_campaign_policy()


@mcp.prompt()
def campaign_summary(campaign_id: int):
    return generate_campaign_summary_prompt(campaign_id)


if __name__ == "__main__":
    mcp.run()