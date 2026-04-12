import pandas as pd


def apply_alert_filters(
    df: pd.DataFrame,
    severity_filter=None,
    status_filter=None,
    start_date=None,
    end_date=None,
    site_filter=None,
) -> pd.DataFrame:
    if df.empty:
        return df

    filtered_df = df.copy()

    if severity_filter:
        filtered_df = filtered_df[filtered_df["severity"].isin(severity_filter)]

    if status_filter and "status" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]

    if site_filter and "location_name" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["location_name"].isin(site_filter)]

    if start_date is not None and end_date is not None and "alert_date" in filtered_df.columns:
        filtered_df["alert_date"] = pd.to_datetime(filtered_df["alert_date"])
        filtered_df = filtered_df[
            (filtered_df["alert_date"].dt.date >= start_date) &
            (filtered_df["alert_date"].dt.date <= end_date)
        ]
        filtered_df["alert_date"] = filtered_df["alert_date"].dt.strftime("%Y-%m-%d")

    return filtered_df