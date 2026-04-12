import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from services.area_service import get_active_monitored_areas


load_dotenv()


def fetch_live_fire_alerts(limit: int = 500) -> pd.DataFrame:
    api_key = os.getenv("GFW_API_KEY")
    if not api_key:
        raise ValueError("Missing GFW_API_KEY in .env")

    areas = get_active_monitored_areas()
    if not areas:
        raise ValueError("No active monitored areas found.")

    dataset = "nasa_viirs_fire_alerts"
    version = "v20240815"
    url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/query/json"

    start_date = (datetime.utcnow() - timedelta(days=14)).strftime("%Y-%m-%d")

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }

    all_rows = []

    for area in areas:
        geometry = area["geojson"]["features"][0]["geometry"]

        payload = {
            "geometry": geometry,
            "sql": f"""
                SELECT
                    latitude,
                    longitude,
                    alert__date AS alert_date,
                    alert__time_utc AS alert_time_utc,
                    confidence__cat AS confidence_cat,
                    "v20240815"."frp__MW" AS frp_mw,
                    alert__count AS alert_count
                FROM results
                WHERE alert__date >= '{start_date}'
                LIMIT {limit}
            """
        }

        params = {
            "page[number]": 1,
            "page[size]": limit
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            params=params,
            timeout=120
        )

        print(f"FIRE STATUS ({area['area_name']}):", response.status_code)

        response.raise_for_status()

        rows = response.json().get("data", [])

        # Attach site name
        for r in rows:
            r["site_name"] = area["area_name"]

        all_rows.extend(rows)

    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    df = fetch_live_fire_alerts(limit=20)
    print(df.head())
    print("Total rows fetched:", len(df))