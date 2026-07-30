import os
from pydantic import BaseModel, Field, ConfigDict
from mcp_server.rag.keyword_search import KeywordStore

knowledge_store = KeywordStore()

def load_and_index_docs_folder():
    """Reads all markdown files inside the project's docs folder and indexes them."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    docs_path = os.path.join(base_dir, "docs")
    
    if not os.path.exists(docs_path):
        print(f"❌ Docs folder not found at: {docs_path}")
        return
        
    for filename in os.listdir(docs_path):
        if filename.endswith(".md"):
            file_path = os.path.join(docs_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Split markdown content into chunks by line
            chunks = [line.strip() for line in content.split("\n") if line.strip()]
            for chunk in chunks:
                knowledge_store.upsert(
                    payload=chunk,
                    metadata={
                        "entity_id": "campaign_1",
                        "role_required": "any",
                    },
                )
                
load_and_index_docs_folder()

class SearchKnowledgeBaseInput(BaseModel):
    query: str = Field(..., description="Keywords to search for in documentation")
    entity_id: str = Field(..., description="Scope search to this entity only")
    top_k: int = Field(default=3, ge=1, le=10)

    model_config = ConfigDict(extra="forbid")

def search_knowledge_base_handler(args: dict, session_role: str) -> str:
    parsed = SearchKnowledgeBaseInput.model_validate(args)

    matches = knowledge_store.query(
        query_text=parsed.query,
        top_k=parsed.top_k,
        filter={"entity_id": parsed.entity_id},
    )

    visible = [
        m for m in matches
        if m["metadata"]["role_required"] in ("any", session_role)
    ]

    if not visible:
        return "No relevant records found for this query or insufficient permissions."

    return "\n\n".join(m["payload"] for m in visible)