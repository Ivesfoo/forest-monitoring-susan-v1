import streamlit as st
from services.notification_read_service import (
    get_unseen_notification_events,
    mark_notification_events_seen,
)


@st.fragment(run_every=10)
def render_live_notification_toasts():
    events = get_unseen_notification_events(limit=2)

    if not events:
        return

    shown_ids = []

    for event in events:
        st.toast(event["message"], icon="🚨")
        shown_ids.append(event["id"])

    mark_notification_events_seen(shown_ids)