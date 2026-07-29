from db.database import get_connection


def authenticate(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


def is_admin(user):
    return user and user["role"] == "admin"


def is_manager(user):
    return user and user["role"] == "manager"


def is_employee(user):
    return user and user["role"] == "employee"