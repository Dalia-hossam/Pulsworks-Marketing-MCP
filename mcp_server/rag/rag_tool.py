"""
RAG Knowledge Base Handler using BM25 keyword search.
"""
from db.database import get_connection
from mcp_server.rag.keyword_search import KeywordStore
from mcp_server.validation import SearchKnowledgeBaseInput
from mcp_server.auth import session

knowledge_store = KeywordStore()


def index_campaign_data():
    """Seed BM25 index with unstructured campaign notes and logs from DB."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cr.campaign_id, c.campaign_name, cr.clicks, cr.conversions, cr.revenue, cust.company
        FROM campaign_results cr
        JOIN campaigns c ON cr.campaign_id = c.id
        JOIN customers cust ON cr.customer_id = cust.id
    """)
    rows = cursor.fetchall()
    conn.close()

    for r in rows:
        text = (
            f"Campaign '{r['campaign_name']}' performance note: Generated {r['conversions']} conversions "
            f"and ${r['revenue']} revenue from client {r['company']}. Total clicks recorded: {r['clicks']}."
        )
        # Higher role requirement for confidential financial metrics
        role_req = "MANAGER" if r['revenue'] > 5000.0 else "ANALYST"
        
        knowledge_store.upsert(
            payload=text,
            metadata={"campaign_id": r["campaign_id"], "role_required": role_req}
        )


def search_knowledge_base_handler(args: dict) -> str:
    """MCP tool handler for knowledge base search."""
    parsed = SearchKnowledgeBaseInput.model_validate(args)

    matches = knowledge_store.query(
        query_text=parsed.query,
        top_k=parsed.top_k,
        filter={"campaign_id": parsed.campaign_id}
    )

    # Server-side authorization filtering in handler[cite: 3]
    allowed_roles = {"ANALYST": ("ANALYST",), "MANAGER": ("ANALYST", "MANAGER"), "ADMIN": ("ANALYST", "MANAGER", "ADMIN")}
    user_allowed = allowed_roles.get(session.role, ("ANALYST",))

    visible = [
        m for m in matches 
        if m["metadata"]["role_required"] in user_allowed
    ]

    if not visible:
        return "No relevant or authorized records found matching your query."

    return "\n\n".join(m["payload"] for m in visible)