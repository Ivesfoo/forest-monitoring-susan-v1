import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY")
if not API_KEY:
    raise ValueError("Missing GFW_API_KEY in .env")

dataset = "gfw_integrated_alerts"
version = "v20260331"

headers = {"x-api-key": API_KEY}
url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/fields"

response = requests.get(url, headers=headers, timeout=60)

print("STATUS:", response.status_code)
print(response.text[:5000])