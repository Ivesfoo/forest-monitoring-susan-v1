import streamlit as st
import pandas as pd


def render_home_type_summary(df: pd.DataFrame):
    st.subheader("Alerts by Type")

    if df.empty or "alert_type" not in df.columns:
        st.info("No alert type data available.")
        return

    summary_df = (
        df["alert_type"]
        .value_counts()
        .reset_index()
    )
    summary_df.columns = ["alert_type", "count"]

    st.dataframe(summary_df, use_container_width=True)


def render_home_status_summary(df: pd.DataFrame):
    st.subheader("Alerts by Status")

    if df.empty or "status" not in df.columns:
        st.info("No status data available.")
        return

    summary_df = (
        df["status"]
        .value_counts()
        .reset_index()
    )
    summary_df.columns = ["status", "count"]

    st.dataframe(summary_df, use_container_width=True)