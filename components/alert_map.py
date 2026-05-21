import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from shapely.geometry import shape
from services.area_service import get_active_monitored_areas


def get_color(severity):
    if severity == "High":
        return "red"
    elif severity == "Medium":
        return "orange"
    return "green"


def get_radius(severity):
    if severity == "High":
        return 3000
    elif severity == "Medium":
        return 2000
    return 1000


def get_status_badge(status):
    if status == "new":
        return "<span style='color:#4ea1ff; font-weight:bold;'>NEW</span>"
    elif status == "reviewed":
        return "<span style='color:#ffb347; font-weight:bold;'>REVIEWED</span>"
    elif status == "resolved":
        return "<span style='color:#7CFC98; font-weight:bold;'>RESOLVED</span>"
    return f"<span style='font-weight:bold;'>{status}</span>"


def build_popup_html(row):
    severity = row.get("severity", "Low")
    status = row.get("status", "unknown")
    location_name = row.get("location_name", "N/A")

    return f"""
    <div style="font-family: Arial; font-size: 13px; min-width: 180px;">
        <b>Alert ID:</b> {row.get('alert_id', 'N/A')}<br>
        <b>Site:</b> {location_name}<br>
        <b>Type:</b> {row.get('alert_type', 'N/A')}<br>
        <b>Severity:</b> {severity}<br>
        <b>Status:</b> {get_status_badge(status)}<br>
        <b>Date:</b> {row.get('alert_date', 'N/A')}<br>
        <b>Source:</b> {row.get('source', 'N/A')}<br>
        <b>Lat:</b> {row.get('latitude', 'N/A')}<br>
        <b>Lon:</b> {row.get('longitude', 'N/A')}
    </div>
    """


def _get_filtered_areas(selected_sites=None):
    areas = get_active_monitored_areas()

    if selected_sites:
        areas = [area for area in areas if area["area_name"] in selected_sites]

    return areas


def _get_map_center(df: pd.DataFrame, areas: list):
    if not df.empty and all(col in df.columns for col in ["latitude", "longitude"]):
        return df["latitude"].mean(), df["longitude"].mean()

    if areas:
        first_geom = areas[0]["geojson"]["features"][0]["geometry"]
        centroid = shape(first_geom).centroid
        return centroid.y, centroid.x

    return 4.7, 101.8


def render_alert_map(
    df: pd.DataFrame,
    title: str = "Alert Locations",
    show_site_polygons: bool = True,
    show_site_labels: bool = True,
    selected_sites=None,
):
    st.subheader(title)

    areas = _get_filtered_areas(selected_sites)

    if df.empty and not areas:
        st.info("No map data available.")
        return

    center_lat, center_lon = _get_map_center(df, areas)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        max_zoom=22,
        detect_retina=True,
        control_scale=True,
        prefer_canvas=True
    )

    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=False,
        control=True,
        max_zoom=22,
        max_native_zoom=22
    ).add_to(m)

    if show_site_polygons:
        for area in areas:
            feature_collection = area["geojson"]
            area_name = area["area_name"]

            folium.GeoJson(
                data=feature_collection,
                name=area_name,
                style_function=lambda x: {
                    "color": "#ff4d4d",
                    "weight": 2,
                    "fillColor": "#ff4d4d",
                    "fillOpacity": 0.08,
                },
                tooltip=folium.Tooltip(area_name, sticky=True),
            ).add_to(m)

            if show_site_labels:
                geom = feature_collection["features"][0]["geometry"]
                centroid = shape(geom).centroid

                folium.Marker(
                    location=[centroid.y, centroid.x],
                    icon=folium.DivIcon(
                        html=f"""
                        <div style="
                            font-size: 12px;
                            font-weight: bold;
                            color: white;
                            text-shadow:
                                -1px -1px 0 #000,
                                 1px -1px 0 #000,
                                -1px  1px 0 #000,
                                 1px  1px 0 #000;
                            white-space: nowrap;
                        ">
                            {area_name}
                        </div>
                        """
                    ),
                ).add_to(m)

    if not df.empty and all(col in df.columns for col in ["latitude", "longitude"]):
        for _, row in df.iterrows():
            severity = row.get("severity", "Low")
            color = get_color(severity)
            radius = get_radius(severity)
            popup_html = build_popup_html(row)

            folium.Circle(
                location=[row["latitude"], row["longitude"]],
                radius=radius,
                color=color,
                weight=2,
                fill=True,
                fill_color=color,
                fill_opacity=0.15,
                popup=popup_html,
            ).add_to(m)

            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.9,
                popup=popup_html,
            ).add_to(m)

    st_folium(m, height=550, use_container_width=True)