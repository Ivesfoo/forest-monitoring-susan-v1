import json
from database.connection import get_connection


def get_active_monitored_areas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, area_name, geojson
        FROM monitored_areas
        WHERE is_active = 1
    """)

    rows = cursor.fetchall()
    conn.close()

    areas = []
    for row in rows:
        areas.append({
            "id": row["id"],
            "area_name": row["area_name"],
            "geojson": json.loads(row["geojson"])
        })

    return areas