import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY", "").strip()

if not API_KEY:
    raise ValueError("Missing GFW_API_KEY in .env")

url = "https://data-api.globalforestwatch.org/v1/dataset/nasa_viirs_fire_alerts/latest"

headers = {
    "x-api-key": API_KEY
}

response = requests.get(url, headers=headers, timeout=60)

print("Status code:", response.status_code)
print("Response preview:", response.text[:1000])