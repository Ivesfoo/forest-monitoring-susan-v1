from database.connection import get_connection


def get_unseen_notification_events(limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, alert_id, event_type, message, is_seen, created_at
        FROM notification_events
        WHERE is_seen = 0
        ORDER BY id ASC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def mark_notification_events_seen(event_ids):
    if not event_ids:
        return

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join(["?"] * len(event_ids))
    query = f"""
        UPDATE notification_events
        SET is_seen = 1
        WHERE id IN ({placeholders})
    """

    cursor.execute(query, event_ids)
    conn.commit()
    conn.close()