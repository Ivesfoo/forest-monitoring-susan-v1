import streamlit as st
from services.alert_service import change_alert_status


def render_status_update_form(alert_ids: list[str]):
    st.subheader("Update Alert Status")

    if not alert_ids:
        st.info("No alert IDs available for update.")
        return

    with st.form("status_update_form"):
        selected_alert_id = st.selectbox("Alert ID", options=alert_ids)
        new_status = st.selectbox("New Status", ["new", "reviewed", "resolved"])
        submitted = st.form_submit_button("Update Status")

        if submitted:
            success = change_alert_status(selected_alert_id, new_status)
            if success:
                st.success(f"Status updated for {selected_alert_id} → {new_status}")
            else:
                st.error(f"Alert ID '{selected_alert_id}' not found.")