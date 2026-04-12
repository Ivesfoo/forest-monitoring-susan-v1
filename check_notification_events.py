from database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT id, alert_id, event_type, message, is_seen, created_at
FROM notification_events
ORDER BY id DESC
""")

rows = cursor.fetchall()

print("Notification events:")
for row in rows:
    print(dict(row))

conn.close()