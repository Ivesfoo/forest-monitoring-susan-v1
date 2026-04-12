from database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT alert_id, alert_type, alert_date, severity, confidence, source
FROM monitoring_alerts
WHERE alert_type = 'fire'
ORDER BY alert_date DESC
LIMIT 10
""")

rows = cursor.fetchall()

print("Latest fire alerts:")
for row in rows:
    print(dict(row))

conn.close()