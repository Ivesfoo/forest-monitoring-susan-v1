import streamlit as st
from utils.page_style import apply_page_style
from services.alert_service import load_alerts_by_type, load_all_alerts, get_sites
from services.filter_service import apply_alert_filters
from components.metric_cards import render_alert_kpis
from components.filters import render_alert_filters
from components.alert_map import render_alert_map
from components.summary_panel import render_alert_summary_panel
from components.alert_table import render_alert_table

st.set_page_config(page_title="Deforestation", page_icon="🌲", layout="wide")
apply_page_style()

st.title("🌲 Deforestation Alerts")

# -----------------------------
# Load data
# -----------------------------
defor_df = load_alerts_by_type("deforestation")
all_alerts_df = load_all_alerts()

if all_alerts_df.empty:
    st.warning("No monitoring alerts found in the system.")
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

# -----------------------------
# Prepare date fields
# -----------------------------
if not defor_df.empty and "alert_date" in defor_df.columns:
    defor_df["alert_date"] = defor_df["alert_date"].astype(str)

if "alert_date" in all_alerts_df.columns:
    all_alerts_df["alert_date"] = all_alerts_df["alert_date"].astype(str)

# -----------------------------
# Small live-data summary
# -----------------------------
site_filtered_defor_df = apply_alert_filters(
    defor_df,
    site_filter=selected_sites,
)

live_df = (
    site_filtered_defor_df[
        site_filtered_defor_df["source"].astype(str).str.contains("Live API", case=False, na=False)
    ]
    if not site_filtered_defor_df.empty and "source" in site_filtered_defor_df.columns
    else site_filtered_defor_df.iloc[0:0]
)

summary_col1, summary_col2 = st.columns(2)
with summary_col1:
    st.info(f"Live Deforestation Alerts: {len(live_df)}")

# -----------------------------
# Filters
# -----------------------------
st.markdown("## Filters")
selected_severity, selected_status, start_date, end_date = render_alert_filters(all_alerts_df)

filtered_defor_df = apply_alert_filters(
    defor_df,
    severity_filter=selected_severity,
    status_filter=selected_status,
    start_date=start_date,
    end_date=end_date,
    site_filter=selected_sites,
)

filtered_activity_df = apply_alert_filters(
    all_alerts_df,
    severity_filter=selected_severity,
    status_filter=selected_status,
    start_date=start_date,
    end_date=end_date,
    site_filter=selected_sites,
)

# -----------------------------
# Sorting
# -----------------------------
if not filtered_defor_df.empty:
    sort_columns = []
    ascending_values = []

    if "alert_date" in filtered_defor_df.columns:
        sort_columns.append("alert_date")
        ascending_values.append(False)

    if "alert_id" in filtered_defor_df.columns:
        sort_columns.append("alert_id")
        ascending_values.append(False)

    if sort_columns:
        filtered_defor_df = filtered_defor_df.sort_values(
            by=sort_columns,
            ascending=ascending_values
        ).reset_index(drop=True)

# -----------------------------
# Alert Overview
# -----------------------------
st.markdown("## Alert Overview")

if filtered_defor_df.empty:
    zero_kpis = {
        "total": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }
    render_alert_kpis(zero_kpis)

    st.info("No deforestation alerts found for the selected site(s) and filters.")

    st.markdown("## Selected Monitoring Sites")
    site_map_df = build_site_centroid_df(selected_sites)

    if site_map_df.empty:
        st.warning("No monitoring sites available to display.")
    else:
        render_alert_map(site_map_df)

    st.markdown("## Deforestation Alert Records")
    st.info("No deforestation alert records available for the selected site(s) and filters.")

else:
    kpis = {
        "total": len(filtered_defor_df),
        "high": int((filtered_defor_df["severity"] == "High").sum()),
        "medium": int((filtered_defor_df["severity"] == "Medium").sum()),
        "low": int((filtered_defor_df["severity"] == "Low").sum()),
    }
    render_alert_kpis(kpis)

    st.markdown("## Alert Trend")
    trend_df = prepare_daily_alert_trend(filtered_defor_df)
    render_alert_trend_chart(trend_df, title="Deforestation Alerts by Date")

    map_col, summary_col = st.columns([3, 1.2], gap="large")

    with map_col:
        render_alert_map(filtered_defor_df, title="Deforestation Alert Locations")

    with summary_col:
        render_alert_summary_panel(filtered_defor_df, panel_title="Quick Summary")
        st.markdown("---")
        defor_alert_ids = sorted(filtered_defor_df["alert_id"].dropna().unique().tolist())
        render_status_update_form(defor_alert_ids)

    st.markdown("## Deforestation Alert Records")
    render_alert_table(filtered_defor_df, title="Deforestation Alerts Data", show_title=False)