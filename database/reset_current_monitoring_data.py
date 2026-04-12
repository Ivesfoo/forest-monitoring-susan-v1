from database.connection import get_connection

def reset_current_monitoring_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notification_events")
    cursor.execute("DELETE FROM monitoring_alerts")

    conn.commit()
    conn.close()

    print("monitoring_alerts and notification_events cleared successfully.")

if __name__ == "__main__":
    reset_current_monitoring_data()