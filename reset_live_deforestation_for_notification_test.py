from database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

# Delete live deforestation alerts only
cursor.execute("""
DELETE FROM monitoring_alerts
WHERE alert_type = 'deforestation'
AND source = 'GFW DIST Live API'
""")

deleted_alerts = cursor.rowcount

# Delete related deforestation notification events
cursor.execute("""
DELETE FROM notification_events
WHERE event_type = 'deforestation_alert'
""")

deleted_events = cursor.rowcount

conn.commit()
conn.close()

print(f"Deleted {deleted_alerts} live deforestation alerts.")
print(f"Deleted {deleted_events} deforestation notification events.")