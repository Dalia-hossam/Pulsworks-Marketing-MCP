from db.database import get_connection

class UserSession:
    """Stores active user session context in the MCP Server."""
    def __init__(self):
        self.current_user = None

    def set_user(self, user):
        old_role = self.current_user["role"] if self.current_user else None
        self.current_user = dict(user) if user else None
        new_role = self.current_user["role"] if self.current_user else None

        # Return True if role changed (triggers notifications/tools/list_changed)
        return old_role != new_role


# Global active session instance
active_session = UserSession()


def authenticate(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, username, role FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        # Convert row object to dictionary
        user_dict = dict(user)
        role_changed = active_session.set_user(user_dict)
        return user_dict, role_changed

    return None, False


def get_active_user():
    return active_session.current_user


def is_admin(user=None):
    user = user or active_session.current_user
    return bool(user and user["role"].upper() == "ADMIN")


def is_manager(user=None):
    user = user or active_session.current_user
    return bool(user and user["role"].upper() in ["ADMIN", "MANAGER"])


def is_analyst(user=None):
    user = user or active_session.current_user
    return bool(user and user["role"].upper() in ["ADMIN", "MANAGER", "ANALYST"])