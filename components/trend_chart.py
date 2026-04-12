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

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    ax.plot(
        trend_df["alert_date"],
        trend_df["count"],
        marker="o",
        linewidth=2,
        markersize=6,
        label="Alerts",
    )

    ax.set_title(title, color="white", fontsize=12, pad=12)
    ax.set_xlabel("Alert Date", color="white")
    ax.set_ylabel("Alert Count", color="white")

    ax.tick_params(axis="x", colors="white", rotation=45)
    ax.tick_params(axis="y", colors="white")

    ax.grid(True, alpha=0.2)
    for spine in ax.spines.values():
        spine.set_color("#444")

    plt.tight_layout()
    st.pyplot(fig, transparent=True)


def render_alert_type_trend_chart(
    trend_df: pd.DataFrame,
    title: str = "Alert Trend by Type"
):
    st.subheader(title)

    if trend_df.empty:
        st.info("No alert type trend data available.")
        return

    fig, ax = plt.subplots(figsize=(10, 4))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    line_styles = {
        "fire": {"linestyle": "-", "marker": "o"},
        "deforestation": {"linestyle": "--", "marker": "s"},
        "restoration": {"linestyle": ":", "marker": "^"},
    }

    for alert_type in trend_df["alert_type"].unique():
        subset = trend_df[trend_df["alert_type"] == alert_type]
        style = line_styles.get(alert_type, {"linestyle": "-", "marker": "o"})

        ax.plot(
            subset["alert_date"],
            subset["count"],
            linewidth=2,
            markersize=7,
            label=alert_type,
            linestyle=style["linestyle"],
            marker=style["marker"],
        )

    ax.set_title(title, color="white", fontsize=12, pad=12)
    ax.set_xlabel("Alert Date", color="white")
    ax.set_ylabel("Alert Count", color="white")

    ax.tick_params(axis="x", colors="white", rotation=45)
    ax.tick_params(axis="y", colors="white")

    ax.grid(True, alpha=0.2)
    for spine in ax.spines.values():
        spine.set_color("#444")

    legend = ax.legend()
    plt.setp(legend.get_texts(), color="white")
    legend.get_frame().set_facecolor("#0E1117")
    legend.get_frame().set_edgecolor("#444")

    plt.tight_layout()
    st.pyplot(fig, transparent=True)