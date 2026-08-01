"""
MCP Protocol Client implementation.
"""
from mcp_server.server import process_rpc
from mcp_server.auth import session


class MCPClient:
    def __init__(self, client_id: str, capabilities: dict = None):
        self.client_id = client_id
        self.capabilities = capabilities if capabilities is not None else {"elicitation": True, "sampling": True}
        self.server_capabilities = {}

    def connect(self):
        resp = process_rpc({
            "method": "initialize",
            "params": {"capabilities": self.capabilities}
        })
        self.server_capabilities = resp.get("result", {}).get("capabilities", {})
        print(f"[{self.client_id}] Handshake complete. Server capabilities: {self.server_capabilities}")
        return resp

    def switch_user_role(self, user_id: int, username: str, new_role: str):
        """Simulates authenticating as a different user role[cite: 1]."""
        changed = session.authenticate_as(user_id, username, new_role)
        if changed:
            print(f"\n⚡ NOTIFICATION: Push message `notifications/tools/list_changed` received!")
            print(f"User switched to {username} ({new_role}). Refetched tools:")
            tools = self.list_tools()
            print([t['name'] for t in tools if isinstance(t, dict) and 'name' in t])

    def list_tools(self):
        resp = process_rpc({"method": "tools/list"})
        return resp.get("result", {}).get("tools", [])

    def read_resource(self, uri: str):
        """Reads static resources from the MCP server (e.g. policy documents)[cite: 1]."""
        req = {
            "method": "resources/read",
            "params": {"uri": uri}
        }
        resp = process_rpc(req)
        if "result" in resp and "contents" in resp["result"]:
            return resp["result"]["contents"][0].get("text", "")
        return str(resp)

    def on_elicitation_request(self, prompt_text: str) -> bool:
        """Mid-call human signoff callback[cite: 1]."""
        print(f"\n⚠️  [ELICITATION PROMPT]: {prompt_text}")
        # Automatically approves for automated test/demo
        print(">> Operator Action: Approved (Yes)")
        return True

    def on_progress_update(self, progress: int, message: str):
        """Progress callback handler[cite: 1]."""
        print(f"⏳ [PROGRESS {progress}%]: {message}")

    def call_tool(self, name: str, args: dict):
        """Calls an MCP tool and unwraps the text content output[cite: 1]."""
        resp = process_rpc(
            {
                "method": "tools/call",
                "params": {"name": name, "arguments": args}
            },
            progress_cb=self.on_progress_update,
            elicitation_cb=self.on_elicitation_request
        )

        # Handle standard RPC errors safely
        if "error" in resp:
            return f"RPC Error: {resp['error']}"

        # Unwrap response content if present
        if "result" in resp and "content" in resp["result"]:
            content_items = resp["result"]["content"]
            if content_items and len(content_items) > 0:
                return content_items[0].get("text", str(resp["result"]))

        return resp