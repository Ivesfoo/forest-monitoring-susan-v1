import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY")
if not API_KEY:
    raise ValueError("Missing GFW_API_KEY in .env")

dataset = "nasa_viirs_fire_alerts"
version = "v20240815"

sql = """
SELECT
    "v20240815"."latitude" AS latitude,
    "v20240815"."longitude" AS longitude,
    "v20240815"."alert__date" AS alert_date,
    "v20240815"."alert__time_utc" AS alert_time_utc,
    "v20240815"."confidence__cat" AS confidence_cat,
    "v20240815"."bright_ti4__K" AS bright_ti4_K,
    "v20240815"."bright_ti5__K" AS bright_ti5_K,
    "v20240815"."frp__MW" AS frp_MW,
    "v20240815"."alert__count" AS alert_count
FROM "v20240815"
LIMIT 10
""".strip()

encoded_sql = quote(sql)
url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/query/json?sql={encoded_sql}"

headers = {"x-api-key": API_KEY}

response = requests.get(url, headers=headers, timeout=60)

print("STATUS:", response.status_code)
print(response.text[:4000])