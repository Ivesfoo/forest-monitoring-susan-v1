import time
from datetime import datetime
from ingestion.load_live_fire_alerts import load_live_fire_alerts
from ingestion.load_live_deforestation_alerts import load_live_deforestation_alerts


def run_live_ingestion_cycle():
    print("=" * 60)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting live ingestion cycle...")

    try:
        fire_ids = load_live_fire_alerts(limit=500)
        print(f"Fire ingestion complete. Inserted {len(fire_ids)} new alerts.")
    except Exception as e:
        print(f"Fire ingestion failed: {e}")

    try:
        defor_ids = load_live_deforestation_alerts(limit=100)
        print(f"Deforestation ingestion complete. Inserted {len(defor_ids)} new alerts.")
    except Exception as e:
        print(f"Deforestation ingestion failed: {e}")

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cycle complete.")
    print("=" * 60)


if __name__ == "__main__":
    REFRESH_SECONDS = 300  # 5 minutes

    print("Live ingestion loop started.")
    print(f"Refresh interval: {REFRESH_SECONDS} seconds")

    while True:
        run_live_ingestion_cycle()
        print(f"Sleeping for {REFRESH_SECONDS} seconds...\n")
        time.sleep(REFRESH_SECONDS)