import streamlit as st
from utils.page_style import apply_page_style
from services.alert_service import (
    load_all_alerts,
    get_sites,
    get_overview_site_table,
)
from services.kpi_service import calculate_alert_kpis
from services.filter_service import apply_alert_filters
from services.trend_service import prepare_alert_type_trend
from components.metric_cards import render_alert_kpis
from components.alert_table import render_alert_table
from components.alert_type_summary import render_alert_type_summary
from components.status_summary import render_status_summary
from components.filters import render_alert_filters
from components.alert_map import render_alert_map
from components.summary_panel import render_alert_summary_panel
from components.export_buttons import render_csv_download_button
from components.trend_chart import render_alert_type_trend_chart

st.set_page_config(page_title="Overview", page_icon="🌍", layout="wide")
apply_page_style()

st.title("🌍 Overview")

df = load_all_alerts()

if df.empty:
    st.warning("No alerts found in the monitoring system.")
    st.stop()

# -----------------------------
# Site Filter
# -----------------------------
site_options = get_sites()
selected_sites = st.multiselect(
    "Select Site(s)",
    options=site_options,
    default=site_options,
)

st.markdown("## Filters")
selected_severity, selected_status, start_date, end_date = render_alert_filters(df)

filtered_df = apply_alert_filters(
    df,
    severity_filter=selected_severity,
    status_filter=selected_status,
    start_date=start_date,
    end_date=end_date,
    site_filter=selected_sites,
)

if filtered_df.empty:
    st.warning("No alerts match the selected filters.")
    st.stop()

st.markdown("## Monitoring Overview")
kpis = calculate_alert_kpis(filtered_df)

# Add active sites count into KPI dict if useful for your KPI renderer
kpis["active_sites"] = len(selected_sites) if selected_sites else 0

render_alert_kpis(kpis)

# -----------------------------
# Site Summary Table
# -----------------------------
st.markdown("## Site Summary")
site_summary_df = get_overview_site_table()

if not site_summary_df.empty and selected_sites:
    site_summary_df = site_summary_df[
        site_summary_df["location_name"].isin(selected_sites)
    ]

if not site_summary_df.empty:
    st.dataframe(site_summary_df, use_container_width=True)
else:
    st.info("No site summary available.")

# -----------------------------
# Trend
# -----------------------------
st.markdown("## Alert Trend")
trend_df = prepare_alert_type_trend(filtered_df)
render_alert_type_trend_chart(trend_df, title="Alerts by Date and Type")

# -----------------------------
# Map + Summary
# -----------------------------
map_col, summary_col = st.columns([3, 1.2], gap="large")

with map_col:
    render_alert_map(filtered_df, title="Monitoring Alert Locations")

with summary_col:
    render_alert_summary_panel(
        filtered_df,
        panel_title="System Summary",
        show_type_counts=True,
    )

# -----------------------------
# Additional Summaries
# -----------------------------
summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.markdown("## Alert Type Summary")
    render_alert_type_summary(filtered_df, show_title=False)

with summary_col2:
    st.markdown("## Status Summary")
    render_status_summary(filtered_df, show_title=False)

# -----------------------------
# Export
# -----------------------------
st.markdown("## Export")
render_csv_download_button(
    filtered_df,
    filename="monitoring_alerts_filtered.csv",
    label="Download Filtered Alerts CSV",
)

# -----------------------------
# Recent Alerts
# -----------------------------
st.markdown("## Recent Monitoring Alerts")
render_alert_table(filtered_df, title="Recent Monitoring Alerts", show_title=False)