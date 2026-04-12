import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def render_alert_trend_chart(
    trend_df: pd.DataFrame,
    title: str = "Alert Trend Over Time"
):
    st.subheader(title)

    if trend_df.empty:
        st.info("No trend data available.")
        return

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(trend_df["alert_date"], trend_df["count"], marker="o")
    ax.set_xlabel("Alert Date")
    ax.set_ylabel("Alert Count")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)