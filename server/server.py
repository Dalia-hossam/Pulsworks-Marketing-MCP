from mcp.server.fastmcp import FastMCP

from server.tools import get_campaigns, get_campaign, approve_campaign,change_role, generate_campaign_report
from server.resources import get_campaign_policy
from server.prompts import generate_campaign_summary_prompt


# Create MCP Server
mcp = FastMCP("PulseWorks Marketing MCP")


# ----------------------
# Tools
# ----------------------

@mcp.tool()
def list_campaigns():
    """Return all marketing campaigns."""
    return get_campaigns()


@mcp.tool()
def campaign_details(campaign_id: int):
    """Return details of one campaign."""
    return get_campaign(campaign_id)


@mcp.tool()
def approve_campaign_tool(username: str, password: str, campaign_id: int):
    """Approve a campaign (Admin only)."""
    from server.auth import authenticate

    user = authenticate(username, password)

    if not user:
        raise ValueError("Invalid username or password.")

    return approve_campaign(user, campaign_id)

@mcp.tool()
def set_role(role: str):
    """Change current user role."""
    return change_role(role)

@mcp.tool()
def campaign_report():
    """Generate campaign report."""
    return generate_campaign_report()

# ----------------------
# Resource
# ----------------------

@mcp.resource("policy://campaign")
def campaign_policy():
    """Marketing campaign policy."""
    return get_campaign_policy()


# ----------------------
# Prompt
# ----------------------

@mcp.prompt()
def campaign_summary(campaign_id: int):
    return generate_campaign_summary_prompt(campaign_id)


if __name__ == "__main__":
    mcp.run()

