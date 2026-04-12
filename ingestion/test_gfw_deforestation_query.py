import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY")
if not API_KEY:
    raise ValueError("Missing GFW_API_KEY in .env")

dataset = "gfw_integrated_alerts"
version = "v20260331"

sql = """
SELECT
    "v20260331"."latitude" AS latitude,
    "v20260331"."longitude" AS longitude,
    "v20260331"."area__ha" AS area_ha
FROM "v20260331"
LIMIT 10
""".strip()

encoded_sql = quote(sql)
url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/query/json?sql={encoded_sql}"

headers = {"x-api-key": API_KEY}

response = requests.get(url, headers=headers, timeout=60)

print("STATUS:", response.status_code)
print(response.text[:4000])