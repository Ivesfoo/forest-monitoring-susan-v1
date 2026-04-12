import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY", "").strip()
if not API_KEY:
    raise ValueError("Missing GFW_API_KEY in .env")

headers = {"x-api-key": API_KEY}

for dataset in ["nasa_viirs_fire_alerts", "gfw_integrated_alerts"]:
    url = f"https://data-api.globalforestwatch.org/dataset/{dataset}"
    response = requests.get(url, headers=headers, timeout=60)
    print("\nDATASET:", dataset)
    print("STATUS:", response.status_code)
    print(response.text[:1200])