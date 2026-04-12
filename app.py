import streamlit as st
from utils.page_style import apply_page_style
from services.alert_service import load_all_alerts
from services.kpi_service import calculate_alert_kpis
from components.metric_cards import render_alert_kpis
from components.home_summary import render_home_type_summary, render_home_status_summary
from components.navigation_cards import render_navigation_cards
from components.data_status import render_data_status
from components.live_notification_toast import render_live_notification_toasts
from components.live_notification_panel import render_live_notification_panel
from components.language_switcher import render_language_switcher
from config.translations import t

st.set_page_config(
    page_title="EPH Forest Monitoring",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_page_style()

render_language_switcher()

st.title(t("app_title"))
st.markdown(
    f"""
    {t("welcome")}

    {t("sidebar_intro")}
    - **{t("overview")}**
    - **{t("fire_alerts")}**
    - **{t("deforestation")}**
    - **{t("restoration")}**
    """
)

render_live_notification_toasts()
render_data_status()
render_navigation_cards()

df = load_all_alerts()

if df.empty:
    st.warning("No alerts found in the monitoring system.")
    st.stop()

st.markdown(f"## {t('platform_snapshot')}")
kpis = calculate_alert_kpis(df)
render_alert_kpis(kpis)

col1, col2 = st.columns(2)

with col1:
    render_home_type_summary(df)

with col2:
    render_home_status_summary(df)

render_live_notification_panel()

st.markdown(f"## {t('quick_notes')}")
st.info(
    f"""
    - {t('note_1')}
    - {t('note_2')}
    - {t('note_3')}
    """
)