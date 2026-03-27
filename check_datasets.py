import requests
import os
import json
from dotenv import load_dotenv
import sys

# Ensure UTF-8 output even on Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
load_dotenv()
API_URL_TEMPLATE = "https://app.mspbots.ai/api/v2/datasets/{}/query"
TOKEN = os.environ.get("MSPBOTS_TOKEN")

datasets = [
    {"id": "1773606476737527809", "name": "CW Manage Agreement Recap"},
    {"id": "1450375671767216129", "name": "CW Manage Agreement Data"},
    {"id": "1616108327545921538", "name": "CW Manage Time Entry - Layered"},
    {"id": "1620428003937386497", "name": "Datto Backup Asset Backups"}
]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print(f"{'Dataset Name':<35} | {'Status':<10} | {'Rows (Sample)':<15} | {'Key Columns Found'}")
print("-" * 100)

for ds in datasets:
    url = API_URL_TEMPLATE.format(ds['id'])
    # Query for just 1 row to check existence and schema
    payload = {
        "query": "SELECT * FROM dataset LIMIT 1"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rows = data.get("data", [])
            
            if rows:
                status = "[Active]"
                count = "1+ (Data exists)"
                # Get first 3 columns as sample
                cols = list(rows[0].keys())[:3]
                cols_str = ", ".join(cols) + "..."
            else:
                status = "[Empty]"
                count = "0"
                cols_str = "N/A"
        else:
            status = f"[Error {response.status_code}]"
            count = "N/A"
            cols_str = response.text[:20]
            
    except Exception as e:
        status = "[Failed]"
        count = "N/A"
        cols_str = str(e)[:20]

    print(f"{ds['name']:<35} | {status:<10} | {count:<15} | {cols_str}")
