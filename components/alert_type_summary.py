import streamlit as st
import pandas as pd


def render_alert_type_summary(df: pd.DataFrame, show_title: bool = True):
    if show_title:
        st.subheader("Alert Type Summary")

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