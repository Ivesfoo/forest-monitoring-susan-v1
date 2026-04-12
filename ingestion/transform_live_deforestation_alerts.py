import json
import pandas as pd


def map_deforestation_confidence(confidence_value: str) -> str:
    if not confidence_value:
        return "unknown"

    value = str(confidence_value).lower().strip()

    if value in ["high", "h"]:
        return "high"
    if value in ["nominal", "medium", "m"]:
        return "nominal"
    if value in ["low", "l"]:
        return "low"

    return value


def map_deforestation_severity(intensity_value) -> str:
    try:
        intensity = float(intensity_value)
    except (TypeError, ValueError):
        return "Low"

    # Adjusted thresholds so current live DIST values can produce alerts
    if intensity >= 80:
        return "High"
    if intensity >= 50:
        return "Medium"
    return "Low"


def build_deforestation_alert_id(row) -> str:
    date_part = str(row.get("umd_glad_landsat_alerts__date", "")).replace("-", "")
    lat = round(float(row.get("latitude", 0)), 4)
    lon = round(float(row.get("longitude", 0)), 4)
    return f"DEFOR_{date_part}_{lat}_{lon}"


def transform_live_deforestation_alerts(df: pd.DataFrame, site_name: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    transformed = pd.DataFrame()

    transformed["alert_id"] = df.apply(build_deforestation_alert_id, axis=1)
    transformed["alert_type"] = "deforestation"
    transformed["latitude"] = df["latitude"]
    transformed["longitude"] = df["longitude"]
    transformed["alert_date"] = df["umd_glad_landsat_alerts__date"]
    transformed["severity"] = df["umd_glad_dist_alerts__intensity"].apply(map_deforestation_severity)
    transformed["confidence"] = df["umd_glad_landsat_alerts__confidence"].apply(map_deforestation_confidence)
    transformed["source"] = "GFW DIST Live API"
    transformed["status"] = "new"
    transformed["location_name"] = site_name

    transformed["metadata"] = df.apply(
        lambda row: json.dumps(
            {
                "dist_intensity": row.get("umd_glad_dist_alerts__intensity"),
                "landsat_confidence": row.get("umd_glad_landsat_alerts__confidence"),
                "landsat_date": row.get("umd_glad_landsat_alerts__date"),
            }
        ),
        axis=1,
    )

    return transformed


if __name__ == "__main__":
    from ingestion.fetch_live_deforestation_alerts import fetch_live_deforestation_alerts

    raw_df = fetch_live_deforestation_alerts(limit=3)
    transformed_df = transform_live_deforestation_alerts(raw_df)

    print(transformed_df.head())
    print("Total transformed rows:", len(transformed_df))