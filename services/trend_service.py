import pandas as pd


def prepare_daily_alert_trend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "alert_date" not in df.columns:
        return pd.DataFrame(columns=["alert_date", "count"])

    trend_df = df.copy()
    trend_df["alert_date"] = pd.to_datetime(trend_df["alert_date"], errors="coerce")

    trend_df = (
        trend_df.groupby("alert_date")
        .size()
        .reset_index(name="count")
        .sort_values("alert_date")
    )

    return trend_df


def prepare_alert_type_trend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "alert_date" not in df.columns or "alert_type" not in df.columns:
        return pd.DataFrame(columns=["alert_date", "alert_type", "count"])

    trend_df = df.copy()
    trend_df["alert_date"] = pd.to_datetime(trend_df["alert_date"], errors="coerce")

    trend_df = (
        trend_df.groupby(["alert_date", "alert_type"])
        .size()
        .reset_index(name="count")
        .sort_values(["alert_date", "alert_type"])
    )

    return trend_df