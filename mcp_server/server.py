import json
from mcp.server.fastmcp import FastMCP, Context
from mcp_server.tools import (
    get_campaigns, 
    get_campaign, 
    approve_campaign, 
    change_role, 
    generate_campaign_report
)
import os
from dotenv import load_dotenv

load_dotenv()  
db_path = os.getenv("DB_PATH", "db/marketing.db")

from mcp_server.resources import get_campaign_policy
from mcp_server.prompts import generate_campaign_summary_prompt
from mcp_server.auth import authenticate

mcp = FastMCP("PulseWorks Marketing MCP")


# ----------------------
# Tools
# ----------------------

@mcp.tool()
def list_campaigns():
    """Return all marketing campaigns."""
    return json.dumps(get_campaigns())


@mcp.tool()
def campaign_details(campaign_id: int):
    """Return details and performance for a specific campaign."""
    return json.dumps(get_campaign(campaign_id))


@mcp.tool()
async def approve_campaign_tool(
    username: str, 
    password: str, 
    campaign_id: int, 
    ctx: Context
) -> str:
    """Approve a campaign (Requires Admin or Manager rights)."""
    user, _ = authenticate(username, password)

    if not user:
        raise ValueError("Invalid username or password.")

    res = await approve_campaign(user, campaign_id, ctx)
    return json.dumps(res)


@mcp.tool()
async def set_role(role: str, ctx: Context) -> str:
    """Change current active session role and notify client of tool changes."""
    result, role_changed = change_role(role)
    
    if role_changed and hasattr(ctx.session, 'send_tool_list_changed'):
        await ctx.session.send_tool_list_changed()
        
    return json.dumps(result)


@mcp.tool()
async def campaign_report(ctx: Context) -> str:
    """Generate campaign report with intermediate progress updates."""
    await ctx.report_progress(progress=10, total=100)
    report_data = await generate_campaign_report(ctx)
    await ctx.report_progress(progress=100, total=100)
    return json.dumps(report_data)


# ----------------------
# Resource & Prompt
# ----------------------

@mcp.resource("policy://campaign")
def campaign_policy() -> str:
    """Read-only company marketing campaign and risk compliance policy."""
    return get_campaign_policy()


@mcp.prompt()
def campaign_summary(campaign_id: int):
    """Parameterized starting prompt template for campaign ROI analysis."""
    return generate_campaign_summary_prompt(campaign_id)


if __name__ == "__main__":
    mcp.run()