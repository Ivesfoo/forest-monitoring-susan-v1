def create_notification_event(cursor, alert_id: str, event_type: str, message: str):
    cursor.execute(
        """
        INSERT INTO notification_events (alert_id, event_type, message, is_seen)
        VALUES (?, ?, ?, 0)
        """,
        (alert_id, event_type, message),
    )