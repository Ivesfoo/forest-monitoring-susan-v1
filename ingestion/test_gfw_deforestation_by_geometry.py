import os
import requests
from dotenv import load_dotenv
from services.area_service import get_active_monitored_areas

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY")
if not API_KEY:
    raise ValueError("Missing GFW_API_KEY in .env")

areas = get_active_monitored_areas()
if not areas:
    raise ValueError("No active monitored areas found.")

geometry = areas[0]["geojson"]["features"][0]["geometry"]

dataset = "gfw_integrated_alerts"
version = "v20260331"
url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/query/json"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "geometry": geometry,
    "sql": """
        SELECT 
            latitude, 
            longitude,
            alert_date,
            alert_time_utc,
            confidence_cat,
            alert_count
        FROM data
        LIMIT 10
    """
}

params = {
    "page[number]": 1,
    "page[size]": 10
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    params=params,
    timeout=120
)

print("STATUS:", response.status_code)
print(response.text[:5000])