import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY")
if not API_KEY:
    raise ValueError("Missing GFW_API_KEY in .env")

headers = {"x-api-key": API_KEY}

dataset = "umd_glad_dist_alerts"
url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/latest"

response = requests.get(url, headers=headers, timeout=60)

print("STATUS:", response.status_code)
print(response.json())