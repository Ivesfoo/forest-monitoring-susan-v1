from database.connection import get_connection


def reset_monitored_areas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM monitored_areas")

    conn.commit()
    conn.close()

    print("All monitored areas deleted successfully.")


if __name__ == "__main__":
    reset_monitored_areas()