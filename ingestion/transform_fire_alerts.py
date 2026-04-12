import pandas as pd


def classify_severity(brightness: float) -> str:
    if brightness >= 360:
        return "High"
    elif brightness >= 340:
        return "Medium"
    return "Low"


def transform_fire_alerts(df: pd.DataFrame) -> pd.DataFrame:
    transformed = pd.DataFrame()

    transformed["alert_id"] = df["alert_id"].astype(str)
    transformed["alert_type"] = "fire"
    transformed["latitude"] = df["latitude"]
    transformed["longitude"] = df["longitude"]
    transformed["alert_date"] = df["alert_date"]
    transformed["severity"] = df["brightness"].apply(classify_severity)
    transformed["confidence"] = df["confidence"].astype(str)
    transformed["source"] = df["source"].astype(str)
    transformed["status"] = "new"
    transformed["location_name"] = None
    transformed["metadata"] = df["brightness"].apply(
        lambda x: f'{{"brightness": {x}}}'
    )

    return transformed