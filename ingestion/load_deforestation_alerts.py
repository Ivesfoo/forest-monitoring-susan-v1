import pandas as pd
from database.connection import get_connection
from ingestion.transform_deforestation_alerts import transform_deforestation_alerts


def load_deforestation_alerts(csv_path: str):
    raw_df = pd.read_csv(csv_path)
    transformed_df = transform_deforestation_alerts(raw_df)

    conn = get_connection()
    cursor = conn.cursor()

    inserted_count = 0

    for _, row in transformed_df.iterrows():
        try:
            cursor.execute(
                """
                INSERT INTO monitoring_alerts (
                    alert_id,
                    alert_type,
                    latitude,
                    longitude,
                    alert_date,
                    severity,
                    confidence,
                    source,
                    status,
                    location_name,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["alert_id"],
                    row["alert_type"],
                    row["latitude"],
                    row["longitude"],
                    row["alert_date"],
                    row["severity"],
                    row["confidence"],
                    row["source"],
                    row["status"],
                    row["location_name"],
                    row["metadata"],
                ),
            )
            inserted_count += 1
        except Exception as e:
            print(f"Skipped alert_id {row['alert_id']}: {e}")

    conn.commit()
    conn.close()

    print(f"Inserted {inserted_count} deforestation alerts successfully.")


if __name__ == "__main__":
    load_deforestation_alerts("ingestion/sample_deforestation_alerts.csv")