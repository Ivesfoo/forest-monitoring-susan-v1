import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from config.translations import t


def render_data_status():
    now = datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).strftime("%Y-%m-%d %H:%M:%S")

    st.markdown(f"### {t('data_status')}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(t("last_updated"), now)

    with col2:
        st.success(t("system_active"))