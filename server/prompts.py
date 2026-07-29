def generate_campaign_summary_prompt(campaign_id):
    return f"""
You are a marketing assistant.

Analyze campaign ID {campaign_id}.

Include:
- Campaign status
- Budget utilization
- Performance insights
- Recommendations for improvement

Keep the response professional and concise.
"""