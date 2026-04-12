import pandas as pd


def classify_severity(restored_ha: float) -> str:
    if restored_ha >= 4.5:
        return "High"
    elif restored_ha >= 2.5:
        return "Medium"
    return "Low"


def transform_restoration_alerts(df: pd.DataFrame) -> pd.DataFrame:
    transformed = pd.DataFrame()

    transformed["alert_id"] = df["alert_id"].astype(str)
    transformed["alert_type"] = "restoration"
    transformed["latitude"] = df["latitude"]
    transformed["longitude"] = df["longitude"]
    transformed["alert_date"] = df["alert_date"]
    transformed["severity"] = df["restored_ha"].apply(classify_severity)
    transformed["confidence"] = df["confidence"].astype(str)
    transformed["source"] = df["source"].astype(str)
    transformed["status"] = "new"
    transformed["location_name"] = None
    transformed["metadata"] = df["restored_ha"].apply(
        lambda x: f'{{"restored_ha": {x}}}'
    )

    return transformed