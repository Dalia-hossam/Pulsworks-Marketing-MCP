"""
Pre-commit test suite for MCP Server components.
Run this script with: python test_mcp_server.py
"""
import os
import unittest
from pathlib import Path

from db.database import initialize_database, get_connection
from mcp_server.auth import session
from mcp_server.server import process_rpc
from mcp_server.rag.rag_tool import index_campaign_data as sync_rag_index, search_knowledge_base_handler


class TestMCPServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Re-initialize DB and RAG index prior to running tests."""
        initialize_database()
        sync_rag_index()

    def test_01_database_seed(self):
        """Test DB connection and initial seed data."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM campaigns")
        campaign_count = cursor.fetchone()[0]
        conn.close()

        self.assertGreater(user_count, 0, "Users table should have seed data.")
        self.assertGreater(campaign_count, 0, "Campaigns table should have seed data.")

    def test_02_capability_negotiation(self):
        """Test initialize handshake RPC."""
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"capabilities": {"elicitation": True, "sampling": True}}
        }
        resp = process_rpc(req)
        self.assertIn("result", resp)
        self.assertEqual(resp["result"]["serverInfo"]["name"], "Marketing-MCP-Server")
        self.assertTrue(session.supports_elicitation)

    def test_03_rag_keyword_search(self):
        """Test BM25 search functionality with role-based visibility."""
        # 1. ANALYST should be restricted from seeing high-revenue manager notes
        session.authenticate_as(3, "employee", "ANALYST")
        res_analyst = search_knowledge_base_handler({
            "query": "performance note",
            "campaign_id": 1,
            "top_k": 3
        })
        self.assertIn(
            "No relevant or authorized records", 
            res_analyst, 
            "Analyst should not see manager-restricted notes."
        )

        # 2. MANAGER should be able to view and search performance notes
        session.authenticate_as(2, "manager", "MANAGER")
        res_manager = search_knowledge_base_handler({
            "query": "performance note",
            "campaign_id": 1,
            "top_k": 3
        })
        self.assertIsNotNone(res_manager)
        self.assertNotIn(
            "No relevant or authorized records", 
            res_manager, 
            "Manager should see search results."
        )

    def test_04_defensive_schema_validation(self):
        """Test server rejection on invalid/unexpected inputs (extra="forbid")."""
        # Sending an invalid key 'unexpected_param' should raise or be caught safely
        req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "search_knowledge_base",
                "arguments": {
                    "query": "test",
                    "campaign_id": 1,
                    "unexpected_param": "forbidden"
                }
            }
        }
        with self.assertRaises(Exception):
            process_rpc(req)

    def test_05_elicitation_trigger_and_fallback(self):
        """Test high-budget update blocking when client lacks elicitation."""
        session.authenticate_as(2, "manager", "MANAGER")
        session.supports_elicitation = False  # Client doesn't support elicitation

        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "update_campaign_budget",
                "arguments": {"campaign_id": 1, "new_budget": 20000.0}
            }
        }
        resp = process_rpc(req)
        text_output = resp["result"]["content"][0]["text"]
        self.assertIn("ERROR", text_output, "High budget update should fail when elicitation is disabled.")


if __name__ == "__main__":
    unittest.main()