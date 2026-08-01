"""
Authentication and session state management.
Tracks active user session, role capabilities, and client negotiation capabilities.
"""
from typing import Optional


class SessionState:
    def __init__(self, user_id: int = 3, username: str = "employee", role: str = "ANALYST"):
        self.user_id: int = user_id
        self.username: str = username
        self.role: str = role
        # Capability negotiation flags set during initialize
        self.supports_elicitation: bool = False
        self.supports_sampling: bool = False

    def authenticate_as(self, user_id: int, username: str, new_role: str) -> bool:
        """
        Updates session user and role dynamically.
        Returns True if role changed (signaling a tools/list_changed notification).
        """
        role_changed = self.role != new_role
        self.user_id = user_id
        self.username = username
        self.role = new_role
        return role_changed


# Global session object for the MCP server instance
session = SessionState()