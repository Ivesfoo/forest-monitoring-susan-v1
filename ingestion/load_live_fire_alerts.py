from database.connection import get_connection
from ingestion.fetch_live_fire_alerts import fetch_live_fire_alerts
from ingestion.transform_live_fire_alerts import transform_live_fire_alerts
from services.area_service import get_active_monitored_areas
from services.notification_event_service import create_notification_event
from utils.geo_utils import is_point_in_geojson
import pandas as pd


def load_live_fire_alerts(limit: int = 100):
    raw_df = fetch_live_fire_alerts(limit=limit)

    if raw_df.empty:
        print("No fire alerts fetched.")
        return []

    transformed_parts = []

    for site_name, site_df in raw_df.groupby("site_name"):
        transformed_site_df = transform_live_fire_alerts(site_df, site_name)
        if not transformed_site_df.empty:
            transformed_parts.append(transformed_site_df)

    if not transformed_parts:
        print("No fire alerts fetched.")
        return []

    transformed_df = pd.concat(transformed_parts, ignore_index=True)

    conn = get_connection()
    cursor = conn.cursor()

    new_alert_ids = []
    areas = get_active_monitored_areas()

    for _, row in transformed_df.iterrows():
        inside_area = False

        for area in areas:
            if is_point_in_geojson(row["latitude"], row["longitude"], area["geojson"]):
                inside_area = True
                break

        if not inside_area:
            continue

        cursor.execute(
            "SELECT 1 FROM monitoring_alerts WHERE alert_id = ?",
            (row["alert_id"],),
        )
        exists = cursor.fetchone()

        if exists:
            continue

        cursor.execute(
            """
            INSERT INTO monitoring_alerts (
                alert_id,
                alert_type,
                latitude,
                longitude,
                alert_date,
                severity,
                confidence,
                source,
                status,
                location_name,
                metadata
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["alert_id"],
                row["alert_type"],
                row["latitude"],
                row["longitude"],
                row["alert_date"],
                row["severity"],
                row["confidence"],
                row["source"],
                row["status"],
                row["location_name"],
                row["metadata"],
            ),
        )

        new_alert_ids.append(row["alert_id"])

        if row["severity"] == "High":
            message = (
                f"🔥 New High Fire Alert Detected | "
                f"Site: {row['location_name']} | "
                f"Alert ID: {row['alert_id']} | "
                f"Date: {row['alert_date']} | "
                f"Lat: {row['latitude']} | "
                f"Lon: {row['longitude']}"
            )

            create_notification_event(
                cursor=cursor,
                alert_id=row["alert_id"],
                event_type="high_fire_alert",
                message=message,
            )

    conn.commit()
    conn.close()

    print(f"Inserted {len(new_alert_ids)} new live fire alerts.")
    return new_alert_ids


if __name__ == "__main__":
    inserted = load_live_fire_alerts(limit=500)
    print("New alert IDs:", inserted[:10])