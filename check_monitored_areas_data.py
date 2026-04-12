from database.connection import get_connection
import json
from shapely.geometry import shape

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT id, area_name, geojson, is_active
    FROM monitored_areas
""")

rows = cursor.fetchall()

print("Monitored Areas:\n")

for row in rows:
    print("ID:", row["id"])
    print("Name:", row["area_name"])
    print("Active:", row["is_active"])

    geo = json.loads(row["geojson"])
    geom = shape(geo["features"][0]["geometry"])

    print("Geometry type:", geom.geom_type)
    print("Is valid:", geom.is_valid)
    print("Bounds:", geom.bounds)
    print("Area:", geom.area)

    coords = geo["features"][0]["geometry"]["coordinates"]
    print("Sample coordinates (first 3 points):", coords[0][:3])
    print("-" * 50)

conn.close()