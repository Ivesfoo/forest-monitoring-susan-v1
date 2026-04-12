import pandas as pd
from database.connection import get_connection
from ingestion.transform_fire_alerts import transform_fire_alerts


def load_fire_alerts(csv_path: str):
    raw_df = pd.read_csv(csv_path)
    transformed_df = transform_fire_alerts(raw_df)

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

    print(f"Inserted {inserted_count} fire alerts successfully.")


import os
import requests
import pandas as pd
from urllib.parse import quote
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()


def fetch_live_fire_alerts(limit: int = 500) -> pd.DataFrame:
    api_key = os.getenv("GFW_API_KEY")
    if not api_key:
        raise ValueError("Missing GFW_API_KEY in .env")

    dataset = "nasa_viirs_fire_alerts"
    version = "v20240815"

    # Wider window for testing
    start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")

    sql = f"""
    SELECT
        "v20240815"."latitude" AS latitude,
        "v20240815"."longitude" AS longitude,
        "v20240815"."alert__date" AS alert_date,
        "v20240815"."alert__time_utc" AS alert_time_utc,
        "v20240815"."confidence__cat" AS confidence_cat,
        "v20240815"."bright_ti4__K" AS bright_ti4_k,
        "v20240815"."bright_ti5__K" AS bright_ti5_k,
        "v20240815"."frp__MW" AS frp_mw,
        "v20240815"."alert__count" AS alert_count
    FROM "v20240815"
    WHERE "v20240815"."alert__date" >= DATE '{start_date}'
    LIMIT {limit}
    """.strip()

    encoded_sql = quote(sql)
    url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/query/json?sql={encoded_sql}"

    headers = {"x-api-key": api_key}
    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()

    payload = response.json()
    rows = payload.get("data", [])

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = fetch_live_fire_alerts(limit=20)
    print(df.head())
    print("Total rows fetched:", len(df))