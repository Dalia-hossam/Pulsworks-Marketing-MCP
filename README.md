# Marketing Campaign Management MCP Server

## System Context & Risk Problem Framing
Our marketing team manages active ad campaign budgets across clients. Direct database access poses extreme risks: an unchecked LLM could accidentally wipe out active budgets or pause live revenue-generating campaigns.

We solved this by building an **MCP Server** in front of our database.

## Database & ERD Structure
* **users**: `(id, username, password, role)` (`ANALYST`, `MANAGER`, `ADMIN`)
* **customers**: `(id, full_name, email, company, status)`
* **campaigns**: `(id, campaign_name, start_date, end_date, budget, max_daily_spend, status)`
* **campaign_results**: `(id, campaign_id, customer_id, clicks, conversions, revenue)`
* **audit_logs**: `(id, user_id, action, details, performed_at)`

## Protocol Concerns Implementation Summary

| Tool / Resource | Type | Role Required | Elicitation Trigger | Risk Mitigation / Rationale |
|---|---|---|---|---|
| `search_knowledge_base` | Read-only | `ANALYST`+ | None | Uses BM25 to safely query campaign performance text. Filters rows by role in handler. |
| `update_campaign_budget` | Write | `MANAGER`+ | Budget > $10,000 | Modifies company financial commitments. Triggers `elicitation/create` if > $10k. |
| `pause_campaign` | Write | `MANAGER`+ | None | Pauses campaign spend and records mandatory log in `audit_logs`. |
| `policy://campaign-rules` | Resource | `ANALYST`+ | None | Policy document exposed via `resources/read` for reasoning over spending rules. |

### Capability Fallback Strategy
If a client connects declaring `elicitation: false` during `initialize`, high-budget updates (> $10,000) are blocked by the server handler with a clear error message rather than silently failing or making unsafe changes.

### Transport Rationale
Built with **stdio** for simple local developer usage, designed for easy deployment to **Streamable HTTP** behind auth proxies for multi-team web access.