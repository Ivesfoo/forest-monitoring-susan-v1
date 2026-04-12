import os
from dotenv import load_dotenv

load_dotenv()


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"true", "1", "yes", "y"}


def _to_float(value: str, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class Settings:
    APP_NAME = os.getenv("APP_NAME", "EPH Forest Monitoring V2")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = _to_bool(os.getenv("DEBUG"), default=True)

    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    DB_PATH = os.getenv("DB_PATH", "data/processed/eph_monitoring.db")

    DEFAULT_LAT = _to_float(os.getenv("DEFAULT_LAT"), 4.5)
    DEFAULT_LON = _to_float(os.getenv("DEFAULT_LON"), 102.0)
    DEFAULT_ZOOM = _to_int(os.getenv("DEFAULT_ZOOM"), 6)

    REFRESH_SECONDS = _to_int(os.getenv("REFRESH_SECONDS"), 60)


settings = Settings()