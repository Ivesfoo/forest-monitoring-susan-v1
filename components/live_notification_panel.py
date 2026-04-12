import streamlit as st
from database.connection import get_connection


def get_recent_notification_events(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, alert_id, event_type, message, is_seen, created_at
        FROM notification_events
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def render_live_notification_panel():
    st.markdown("## Recent Notifications")

    events = get_recent_notification_events(limit=10)

    if not events:
        st.info("No notification events yet.")
        return

    for event in events:
        if event["is_seen"] == 0:
            st.warning(f"{event['created_at']} | {event['message']}")
        else:
            st.info(f"{event['created_at']} | {event['message']}")