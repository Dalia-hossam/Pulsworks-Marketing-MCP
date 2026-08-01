"""
MCP Protocol Engine implementation.
"""
from mcp_server.auth import session
from mcp_server.tools import get_available_tools, handle_tool_call
from mcp_server.resources import list_resources, read_resource
from mcp_server.prompts import list_prompts, get_prompt
from mcp_server.rag.rag_tool import search_knowledge_base_handler, index_campaign_data


def initialize(client_capabilities: dict) -> dict:
    """Handles protocol capability negotiation[cite: 1]."""
    session.supports_elicitation = client_capabilities.get("elicitation", False)
    session.supports_sampling = client_capabilities.get("sampling", False)

    index_campaign_data()  # Build search index

    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {"listChanged": True},
            "resources": {},
            "prompts": {},
            "elicitation": {}
        },
        "serverInfo": {"name": "Marketing-MCP-Server", "version": "1.0.0"}
    }


def process_rpc(request: dict, progress_cb=None, elicitation_cb=None) -> dict:
    """Dispatches incoming JSON-RPC 2.0 requests[cite: 1]."""
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id", 1)

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": initialize(params.get("capabilities", {}))}
    
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": get_available_tools()}}
    
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "search_knowledge_base":
            res = search_knowledge_base_handler(args)
        else:
            res = handle_tool_call(tool_name, args, progress_cb, elicitation_cb)
            
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": res}]}}
    
    elif method == "resources/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"resources": list_resources()}}
    
    elif method == "resources/read":
        content = read_resource(params.get("uri"))
        return {"jsonrpc": "2.0", "id": req_id, "result": {"contents": [{"text": content}]}}
    
    elif method == "prompts/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": list_prompts()}}
    
    elif method == "prompts/get":
        prompt_text = get_prompt(params.get("name"), params.get("arguments", {}))
        return {"jsonrpc": "2.0", "id": req_id, "result": {"description": prompt_text}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {method} not found"}}