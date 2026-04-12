from database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("UPDATE notification_events SET is_seen = 0")
conn.commit()
conn.close()

print("All notification events reset to unseen.")