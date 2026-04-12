import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY")

headers = {"x-api-key": API_KEY}

dataset = "nasa_viirs_fire_alerts"

url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/latest"

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print(response.json())