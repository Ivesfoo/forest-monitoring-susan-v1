import streamlit as st
import pandas as pd


def render_alert_filters(df: pd.DataFrame):
    if df.empty:
        return [], [], None, None

    severity_options = ["High", "Medium", "Low"]

    if "status" in df.columns:
        status_options = sorted(df["status"].dropna().unique().tolist())
    else:
        status_options = ["new"]

    if "alert_date" in df.columns:
        date_series = pd.to_datetime(df["alert_date"], errors="coerce")
        min_date = date_series.min().date()
        max_date = date_series.max().date()
    else:
        min_date = None
        max_date = None

    col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])

    with col1:
        selected_severity = st.multiselect(
            "Severity",
            options=severity_options,
            default=severity_options,
        )

    with col2:
        selected_status = st.multiselect(
            "Status",
            options=status_options,
            default=status_options,
        )

    with col3:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
        ) if min_date and max_date else None

    with col4:
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
        ) if min_date and max_date else None

    return selected_severity, selected_status, start_date, end_date