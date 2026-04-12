from database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

# Delete non-live deforestation alerts
cursor.execute("""
DELETE FROM monitoring_alerts
WHERE alert_type = 'deforestation'
AND source NOT LIKE '%Live API%'
""")

deleted_rows = cursor.rowcount

conn.commit()
conn.close()

print(f"Deleted {deleted_rows} seeded deforestation alerts.")