import streamlit as st
import pandas as pd


def style_status(val):
    if val == "new":
        return "background-color: #1f77b4; color: white;"  # blue
    elif val == "reviewed":
        return "background-color: #ff7f0e; color: white;"  # orange
    elif val == "resolved":
        return "background-color: #2ca02c; color: white;"  # green
    return ""


def style_severity(val):
    if val == "High":
        return "color: #ff4d4f; font-weight: bold;"
    elif val == "Medium":
        return "color: #ffa940;"
    elif val == "Low":
        return "color: #73d13d;"
    return ""


def render_alert_table(
    df: pd.DataFrame,
    title: str = "Alerts Data",
    show_title: bool = True,
):
    if show_title:
        st.subheader(title)

    if df.empty:
        st.info("No records found.")
        return

    preferred_columns = [
        "alert_id",
        "alert_type",
        "alert_date",
        "severity",
        "status",
        "latitude",
        "longitude",
        "confidence",
        "source",
    ]

    available_columns = [col for col in preferred_columns if col in df.columns]

    display_df = df[available_columns]

    styled_df = display_df.style

    if "status" in display_df.columns:
        styled_df = styled_df.map(style_status, subset=["status"])

    if "severity" in display_df.columns:
        styled_df = styled_df.map(style_severity, subset=["severity"])

    st.dataframe(styled_df, use_container_width=True)