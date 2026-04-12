from ingestion.load_live_fire_alerts import load_live_fire_alerts
from ingestion.load_live_deforestation_alerts import load_live_deforestation_alerts


def main():
    print("Starting v1 data refresh...")

    try:
        fire_ids = load_live_fire_alerts(limit=500)
        print(f"Fire refresh done. New fire alerts inserted: {len(fire_ids)}")
    except Exception as e:
        print(f"Fire refresh failed: {e}")
        fire_ids = []

    try:
        deforestation_ids = load_live_deforestation_alerts(limit=100)
        print(
            f"Deforestation refresh done. New deforestation alerts inserted: {len(deforestation_ids)}"
        )
    except Exception as e:
        print(f"Deforestation refresh failed: {e}")
        deforestation_ids = []

    print("V1 data refresh completed.")
    print(f"Total new alerts inserted: {len(fire_ids) + len(deforestation_ids)}")


if __name__ == "__main__":
    main()