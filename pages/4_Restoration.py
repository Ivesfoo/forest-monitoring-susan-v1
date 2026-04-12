import streamlit as st
from utils.page_style import apply_page_style
from services.alert_service import load_alerts_by_type
from services.kpi_service import calculate_alert_kpis
from services.filter_service import apply_alert_filters
from services.trend_service import prepare_daily_alert_trend
from components.metric_cards import render_alert_kpis
from components.alert_table import render_alert_table
from components.filters import render_alert_filters
from components.alert_map import render_alert_map
from components.summary_panel import render_alert_summary_panel
from components.export_buttons import render_csv_download_button
from components.trend_chart import render_alert_trend_chart
from components.status_update_form import render_status_update_form

st.set_page_config(page_title="Restoration", page_icon="🌱", layout="wide")
apply_page_style()

st.title("🌱 Restoration Alerts")

df = load_alerts_by_type("restoration")

if df.empty:
    st.warning("No restoration alerts found.")
    st.stop()

st.markdown("## Filters")
selected_severity, selected_status, start_date, end_date = render_alert_filters(df)

filtered_df = apply_alert_filters(
    df,
    severity_filter=selected_severity,
    status_filter=selected_status,
    start_date=start_date,
    end_date=end_date,
)

if filtered_df.empty:
    st.warning("No restoration alerts match the selected filters.")
    st.stop()

st.markdown("## Alert Overview")
kpis = calculate_alert_kpis(filtered_df)
render_alert_kpis(kpis)

st.markdown("## Alert Trend")
trend_df = prepare_daily_alert_trend(filtered_df)
render_alert_trend_chart(trend_df, title="Restoration Alerts by Date")

map_col, summary_col = st.columns([3, 1.2], gap="large")

with map_col:
    render_alert_map(filtered_df, title="Restoration Alert Locations")

with summary_col:
    render_alert_summary_panel(filtered_df, panel_title="Quick Summary")
    st.markdown("---")
    restoration_alert_ids = sorted(filtered_df["alert_id"].dropna().unique().tolist())
    render_status_update_form(restoration_alert_ids)

st.markdown("## Export")
render_csv_download_button(
    filtered_df,
    filename="restoration_alerts_filtered.csv",
    label="Download Restoration Alerts CSV",
)

st.markdown("## Alert Records")
render_alert_table(
    filtered_df,
    title="Restoration Alerts Data",
    show_title=False,
)