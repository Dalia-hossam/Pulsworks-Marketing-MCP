from mcp_server.validation import validate_campaign_input

def generate_campaign_summary_prompt(campaign_id: int) -> str:
    """Generates a structured prompt template for analyzing a marketing campaign's ROI and metrics."""
    # Server-side validation of prompt input parameters
    valid, error = validate_campaign_input({"campaign_id": campaign_id})
    if not valid:
        raise ValueError(f"Invalid prompt argument: {error}")

    return f"""You are a senior marketing performance assistant at Plus Marketing.

Please perform a detailed performance review for Campaign ID: {campaign_id}.

Your analysis must cover the following sections:
1. **Status & Budget Utilization**: Evaluate current spending against total budget limits.
2. **Key Performance Metrics**: Aggregate clicks, impressions, conversion rates, and total revenue.
3. **Strategic Recommendations**: Provide 2-3 actionable optimizations to improve ROI and lower CAC.

Ensure your response is concise, data-backed, and executive-ready."""