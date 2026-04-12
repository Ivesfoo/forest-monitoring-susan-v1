import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GFW_API_KEY")

headers = {"x-api-key": API_KEY}

dataset = "nasa_viirs_fire_alerts"
version = "v20240815"

url = f"https://data-api.globalforestwatch.org/dataset/{dataset}/{version}/fields"

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print(response.json())