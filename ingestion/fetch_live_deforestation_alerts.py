import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
from services.area_service import get_active_monitored_areas

load_dotenv()


def fetch_live_deforestation_alerts(limit: int = 100) -> pd.DataFrame:
    api_key = os.getenv("GFW_API_KEY")
    if not api_key:
        raise ValueError("Missing GFW_API_KEY in .env")

    areas = get_active_monitored_areas()
    if not areas:
        raise ValueError("No active monitored areas found.")

    start_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")

    dataset = "umd_glad_dist_alerts"
    version = "v20260329"
    url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/query/json"

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
                    umd_glad_landsat_alerts__date,
                    umd_glad_landsat_alerts__confidence,
                    umd_glad_dist_alerts__intensity
                FROM results
                WHERE umd_glad_landsat_alerts__date >= '{start_date}'
                ORDER BY umd_glad_landsat_alerts__date DESC
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

        print(f"STATUS ({area['area_name']}):", response.status_code)

        response.raise_for_status()

        rows = response.json().get("data", [])
        # Attach site name to each row
        for r in rows:
            r["site_name"] = area["area_name"]

        all_rows.extend(rows)

    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    df = fetch_live_deforestation_alerts(limit=3)
    print(df.head())
    print("Total rows fetched:", len(df))