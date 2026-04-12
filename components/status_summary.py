import streamlit as st
import pandas as pd


def render_status_summary(df: pd.DataFrame, show_title: bool = True):
    if show_title:
        st.subheader("Status Summary")

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