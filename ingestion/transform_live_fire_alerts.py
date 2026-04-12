import json
import pandas as pd


def map_confidence_to_text(confidence_cat: str) -> str:
    if not confidence_cat:
        return "unknown"

    value = str(confidence_cat).lower()

    if value in ["h", "high"]:
        return "high"
    if value in ["n", "nominal", "medium"]:
        return "nominal"
    if value in ["l", "low"]:
        return "low"

    return value


def map_severity_from_frp(frp_mw) -> str:
    try:
        frp = float(frp_mw)
    except (TypeError, ValueError):
        return "Low"

    if frp >= 10:
        return "High"
    if frp >= 3:
        return "Medium"
    return "Low"


def build_alert_id(row) -> str:
    date_part = str(row.get("alert_date", "")).replace("-", "")
    time_part = str(row.get("alert_time_utc", "0000"))
    lat = round(float(row.get("latitude", 0)), 4)
    lon = round(float(row.get("longitude", 0)), 4)
    return f"FIRE_{date_part}_{time_part}_{lat}_{lon}"


def transform_live_fire_alerts(df: pd.DataFrame, site_name: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    transformed = pd.DataFrame()

    transformed["alert_id"] = df.apply(build_alert_id, axis=1)
    transformed["alert_type"] = "fire"
    transformed["latitude"] = df["latitude"]
    transformed["longitude"] = df["longitude"]
    transformed["alert_date"] = df["alert_date"]
    transformed["severity"] = df["frp_mw"].apply(map_severity_from_frp)
    transformed["confidence"] = df["confidence_cat"].apply(map_confidence_to_text)
    transformed["source"] = "GFW Live API"
    transformed["status"] = "new"
    transformed["location_name"] = site_name

    transformed["metadata"] = df.apply(
        lambda row: json.dumps(
            {
                "alert_time_utc": row.get("alert_time_utc"),
                "bright_ti4_k": row.get("bright_ti4_k"),
                "bright_ti5_k": row.get("bright_ti5_k"),
                "frp_mw": row.get("frp_mw"),
                "alert_count": row.get("alert_count"),
            }
        ),
        axis=1,
    )

    return transformed


if __name__ == "__main__":
    from ingestion.fetch_live_fire_alerts import fetch_live_fire_alerts

    raw_df = fetch_live_fire_alerts(limit=10)
    transformed_df = transform_live_fire_alerts(raw_df)

    print(transformed_df.head())
    print("Total transformed rows:", len(transformed_df))