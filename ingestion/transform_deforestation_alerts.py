import pandas as pd


def classify_severity(tree_loss_ha: float) -> str:
    if tree_loss_ha >= 12:
        return "High"
    elif tree_loss_ha >= 6:
        return "Medium"
    return "Low"


def transform_deforestation_alerts(df: pd.DataFrame) -> pd.DataFrame:
    transformed = pd.DataFrame()

    transformed["alert_id"] = df["alert_id"].astype(str)
    transformed["alert_type"] = "deforestation"
    transformed["latitude"] = df["latitude"]
    transformed["longitude"] = df["longitude"]
    transformed["alert_date"] = df["alert_date"]
    transformed["severity"] = df["tree_loss_ha"].apply(classify_severity)
    transformed["confidence"] = df["confidence"].astype(str)
    transformed["source"] = df["source"].astype(str)
    transformed["status"] = "new"
    transformed["location_name"] = None
    transformed["metadata"] = df["tree_loss_ha"].apply(
        lambda x: f'{{"tree_loss_ha": {x}}}'
    )

    return transformed