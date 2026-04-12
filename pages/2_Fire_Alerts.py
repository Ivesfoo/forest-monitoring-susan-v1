import streamlit as st
import pandas as pd
from shapely.geometry import shape
from utils.page_style import apply_page_style
from services.alert_service import load_alerts_by_type, load_all_alerts, get_sites
from services.filter_service import apply_alert_filters
from services.area_service import get_active_monitored_areas
from components.metric_cards import render_alert_kpis
from components.alert_table import render_alert_table
from components.filters import render_alert_filters
from components.alert_map import render_alert_map
from components.summary_panel import render_alert_summary_panel
from components.trend_chart import render_alert_trend_chart
from components.status_update_form import render_status_update_form
from services.trend_service import prepare_daily_alert_trend

st.set_page_config(page_title="Fire Alerts", page_icon="🔥", layout="wide")
apply_page_style()

st.title("🔥 Fire Alerts")


def build_site_centroid_df(selected_sites: list[str]) -> pd.DataFrame:
    areas = get_active_monitored_areas()
    rows = []

    for area in areas:
        if area["area_name"] not in selected_sites:
            continue

        geom = area["geojson"]["features"][0]["geometry"]
        centroid = shape(geom).centroid

        rows.append(
            {
                "alert_id": f"SITE_{area['area_name']}",
                "alert_type": "monitoring_site",
                "alert_date": None,
                "severity": "Low",
                "status": "active",
                "latitude": centroid.y,
                "longitude": centroid.x,
                "confidence": "",
                "source": "Monitoring Site",
                "location_name": area["area_name"],
            }
        )

    return pd.DataFrame(rows)


# -----------------------------
# Load data
# -----------------------------
fire_df = load_alerts_by_type("fire")
all_alerts_df = load_all_alerts()

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
# Filters
# -----------------------------
# IMPORTANT:
# Use all_alerts_df as filter base so date inputs always have valid dates.
st.markdown("## Filters")
selected_severity, selected_status, start_date, end_date = render_alert_filters(all_alerts_df)

filtered_fire_df = apply_alert_filters(
    fire_df,
    severity_filter=selected_severity,
    status_filter=selected_status,
    start_date=start_date,
    end_date=end_date,
    site_filter=selected_sites,
)

# -----------------------------
# Alert Overview
# -----------------------------
st.markdown("## Alert Overview")

if filtered_fire_df.empty:
    zero_kpis = {
        "total": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }
    render_alert_kpis(zero_kpis)

    st.info("No fire alerts found for the selected site(s) and filters.")

    st.markdown("## Selected Monitoring Sites")
    site_map_df = build_site_centroid_df(selected_sites)

    if site_map_df.empty:
        st.warning("No monitoring sites available to display.")
    else:
        render_alert_map(site_map_df, title="Selected Monitoring Sites")

    st.markdown("## Fire Alert Records")
    st.info("No fire alert records available for the selected site(s) and filters.")

else:
    kpis = {
        "total": len(filtered_fire_df),
        "high": int((filtered_fire_df["severity"] == "High").sum()),
        "medium": int((filtered_fire_df["severity"] == "Medium").sum()),
        "low": int((filtered_fire_df["severity"] == "Low").sum()),
    }
    render_alert_kpis(kpis)

    st.markdown("## Alert Trend")
    trend_df = prepare_daily_alert_trend(filtered_fire_df)
    render_alert_trend_chart(trend_df, title="Fire Alerts by Date")

    map_col, summary_col = st.columns([3, 1.2], gap="large")

    with map_col:
        render_alert_map(filtered_fire_df, title="Fire Alert Locations")

    with summary_col:
        render_alert_summary_panel(filtered_fire_df, panel_title="Quick Summary")
        st.markdown("---")
        fire_alert_ids = sorted(filtered_fire_df["alert_id"].dropna().unique().tolist())
        render_status_update_form(fire_alert_ids)

    st.markdown("## Fire Alert Records")
    render_alert_table(filtered_fire_df, title="Fire Alerts Data", show_title=False)