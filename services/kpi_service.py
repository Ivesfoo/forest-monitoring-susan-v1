import pandas as pd


def calculate_alert_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "total": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

    return {
        "total": len(df),
        "high": len(df[df["severity"] == "High"]),
        "medium": len(df[df["severity"] == "Medium"]),
        "low": len(df[df["severity"] == "Low"]),
    }