import pandas as pd
from database.queries import (
    get_alerts_by_type,
    get_all_alerts,
    get_alerts_by_site,
    get_alerts_by_type_and_site,
    get_active_sites,
    get_site_alert_summary,
    get_overview_counts,
    get_recent_alerts,
    update_alert_status,
)


# =========================
# BASIC LOADERS (existing)
# =========================

def load_alerts_by_type(alert_type: str, site_name: str = None) -> pd.DataFrame:
    if site_name:
        rows = get_alerts_by_type_and_site(alert_type, site_name)
    else:
        rows = get_alerts_by_type(alert_type)

    df = pd.DataFrame([dict(row) for row in rows])

    if not df.empty:
        df = df.sort_values(by="alert_date", ascending=False)

    return df


def load_all_alerts(site_name: str = None) -> pd.DataFrame:
    if site_name:
        rows = get_alerts_by_site(site_name)
    else:
        rows = get_all_alerts()

    df = pd.DataFrame([dict(row) for row in rows])

    if not df.empty:
        df = df.sort_values(by="alert_date", ascending=False)

    return df


def change_alert_status(alert_id: str, new_status: str) -> bool:
    return update_alert_status(alert_id, new_status)


# =========================
# NEW: SITE UTILITIES
# =========================

def get_sites() -> list:
    return get_active_sites()


# =========================
# NEW: OVERVIEW DATA
# =========================

def get_overview_kpis() -> dict:
    row = get_overview_counts()
    return dict(row) if row else {}


def get_overview_site_table() -> pd.DataFrame:
    rows = get_site_alert_summary()
    df = pd.DataFrame([dict(row) for row in rows])

    if not df.empty:
        df = df.sort_values(by="total_alerts", ascending=False)

    return df


def get_recent_alerts_df(limit: int = 10) -> pd.DataFrame:
    rows = get_recent_alerts(limit)
    df = pd.DataFrame([dict(row) for row in rows])

    if not df.empty:
        df = df.sort_values(by="alert_date", ascending=False)

    return df