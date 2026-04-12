import streamlit as st
import pandas as pd


def render_alert_summary_panel(
    df: pd.DataFrame,
    panel_title: str = "Quick Summary",
    show_type_counts: bool = False,
):
    st.subheader(panel_title)

    if df.empty:
        st.info("No summary available.")
        return

    latest_alert = df["alert_date"].max() if "alert_date" in df.columns else "N/A"
    total_alerts = len(df)

    high_count = len(df[df["severity"] == "High"]) if "severity" in df.columns else 0
    medium_count = len(df[df["severity"] == "Medium"]) if "severity" in df.columns else 0
    low_count = len(df[df["severity"] == "Low"]) if "severity" in df.columns else 0

    st.metric("Latest Alert", latest_alert)
    st.metric("Filtered Alerts", total_alerts)

    if show_type_counts and "alert_type" in df.columns:
        st.metric("Alert Types", df["alert_type"].nunique())

    st.markdown("### Severity Legend")
    st.write(f"🔴 High: {high_count}")
    st.write(f"🟠 Medium: {medium_count}")
    st.write(f"🟢 Low: {low_count}")

    if show_type_counts and "alert_type" in df.columns:
        st.markdown("### Types Present")
        type_counts = df["alert_type"].value_counts()
        for alert_type, count in type_counts.items():
            st.write(f"- {alert_type}: {count}")