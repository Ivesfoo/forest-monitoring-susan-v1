from database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("DELETE FROM monitoring_alerts")
cursor.execute("DELETE FROM notification_events")

conn.commit()
conn.close()

print("All alerts deleted successfully.")