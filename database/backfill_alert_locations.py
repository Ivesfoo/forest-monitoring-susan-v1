from database.connection import get_connection
from services.area_service import get_active_monitored_areas
from shapely.geometry import Point, shape


def backfill_alert_locations():
    conn = get_connection()
    cursor = conn.cursor()

    # Get all monitored areas
    areas = get_active_monitored_areas()
    if not areas:
        print("No monitored areas found.")
        return

    # Convert areas into shapely geometries
    area_geometries = []
    for area in areas:
        geom = area["geojson"]["features"][0]["geometry"]
        polygon = shape(geom)
        area_geometries.append({
            "name": area["area_name"],
            "polygon": polygon
        })

    # Get alerts without location_name
    cursor.execute("""
        SELECT id, latitude, longitude
        FROM monitoring_alerts
        WHERE location_name IS NULL OR location_name = ''
    """)

    alerts = cursor.fetchall()

    print(f"Total alerts to process: {len(alerts)}")

    updated_count = 0

    for alert in alerts:
        point = Point(alert["longitude"], alert["latitude"])
        assigned_site = None

        for area in area_geometries:
            if area["polygon"].contains(point):
                assigned_site = area["name"]
                break

        if assigned_site:
            cursor.execute("""
                UPDATE monitoring_alerts
                SET location_name = ?
                WHERE id = ?
            """, (assigned_site, alert["id"]))
            updated_count += 1

    conn.commit()
    conn.close()

    print(f"Updated {updated_count} alerts with site names.")


if __name__ == "__main__":
    backfill_alert_locations()