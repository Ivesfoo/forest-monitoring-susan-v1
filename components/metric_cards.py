import streamlit as st


def render_alert_kpis(kpis: dict):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Alerts", kpis["total"])
    col2.metric("High", kpis["high"])
    col3.metric("Medium", kpis["medium"])
    col4.metric("Low", kpis["low"])