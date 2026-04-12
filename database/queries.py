from database.connection import get_connection


def get_all_alerts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monitoring_alerts ORDER BY alert_date DESC, id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_alerts_by_type(alert_type: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM monitoring_alerts
        WHERE alert_type = ?
        ORDER BY alert_date DESC, id DESC
        """,
        (alert_type,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

#Site-specific data
def get_alerts_by_site(site_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM monitoring_alerts
        WHERE location_name = ?
        ORDER BY alert_date DESC, id DESC
        """,
        (site_name,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fire/Deforstation + Site
def get_alerts_by_type_and_site(alert_type: str, site_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM monitoring_alerts
        WHERE alert_type = ? AND location_name = ?
        ORDER BY alert_date DESC, id DESC
        """,
        (alert_type, site_name),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# Dropdown options
def get_active_sites():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT area_name
        FROM monitored_areas
        WHERE is_active = 1
        ORDER BY area_name
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [row["area_name"] for row in rows]

# Latest alerts panel
def get_recent_alerts(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM monitoring_alerts
        ORDER BY alert_date DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# Overview Table
def get_site_alert_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            location_name,
            COUNT(*) AS total_alerts,
            SUM(CASE WHEN alert_type = 'fire' THEN 1 ELSE 0 END) AS fire_alerts,
            SUM(CASE WHEN alert_type = 'deforestation' THEN 1 ELSE 0 END) AS deforestation_alerts,
            SUM(CASE WHEN severity = 'High' THEN 1 ELSE 0 END) AS high_alerts,
            MAX(alert_date) AS latest_alert_date
        FROM monitoring_alerts
        WHERE location_name IS NOT NULL
        GROUP BY location_name
        ORDER BY total_alerts DESC, location_name ASC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# Top KPI cards
def get_overview_counts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_alerts,
            SUM(CASE WHEN alert_type = 'fire' THEN 1 ELSE 0 END) AS fire_alerts,
            SUM(CASE WHEN alert_type = 'deforestation' THEN 1 ELSE 0 END) AS deforestation_alerts,
            SUM(CASE WHEN severity = 'High' THEN 1 ELSE 0 END) AS high_alerts,
            MAX(alert_date) AS latest_alert_date
        FROM monitoring_alerts
        """
    )
    row = cursor.fetchone()
    conn.close()
    return row


def update_alert_status(alert_id: str, new_status: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE monitoring_alerts
        SET status = ?
        WHERE alert_id = ?
        """,
        (new_status, alert_id),
    )

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated