from db.database import get_connection


def get_all_campaigns():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM campaigns")
    campaigns = cursor.fetchall()

    conn.close()
    return campaigns


def get_campaign_by_id(campaign_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM campaigns WHERE id = ?",
        (campaign_id,)
    )

    campaign = cursor.fetchone()

    conn.close()
    return campaign


def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    conn.close()
    return customers