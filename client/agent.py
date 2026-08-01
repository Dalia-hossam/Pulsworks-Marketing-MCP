# client/agent.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class MarketingAgent:
    def __init__(self, mcp_client):
        self.mcp_client = mcp_client
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
        
        # Initialize Gemini Client if API key exists
        if self.api_key:
            self.genai_client = genai.Client(api_key=self.api_key)
        else:
            self.genai_client = None

    def execute_task(self, tool_name: str, arguments: dict):
        """Executes an MCP tool call through the mcp_client[cite: 1]."""
        print(f"\n[Agent] Executing tool: '{tool_name}' with args: {arguments}")
        result = self.mcp_client.call_tool(tool_name, arguments)
        print(f"[Agent] Result: {result}")
        return result

    def read_policy(self, uri: str = "policy://campaign-rules"):
        """Reads policy documents or resources from the MCP server[cite: 1]."""
        print(f"\n[Agent] Reading resource from URI: '{uri}'")
        content = self.mcp_client.read_resource(uri)
        print(f"[Agent] Resource Content:\n{content}")
        return content

    def ask_gemini(self, prompt: str):
        """Queries Gemini model for natural language reasoning."""
        if not self.genai_client:
            print("[Agent Warning] GEMINI_API_KEY not found in environment.")
            return "API Key missing."
            
        response = self.genai_client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text