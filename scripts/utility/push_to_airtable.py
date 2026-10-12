import os
import requests

def load_env_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env_file(".env")
load_env_file("fair_dinkum_publishing/.env")

API_ROOT = "https://api.airtable.com/v0"
api_key = os.getenv("AIRTABLE_API_KEY")
base_id = os.getenv("AIRTABLE_BASE_ID") or "appqqwluJEP7553HY"
table_id = os.getenv("AIRTABLE_TABLE_ID") or "tblYavj3sIPsQeJcS"

print(f"Base ID: {base_id}")
print(f"Table ID: {table_id}")
print(f"API Key present: {bool(api_key)}")

if not api_key:
    print("[!] AIRTABLE_API_KEY not found in environment or .env files")
else:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    url = f"{API_ROOT}/{base_id}/{table_id}"
    fields = {
        "Name": "The Autonomous Solopreneur: Building & Scaling Multi-Agent AI Enterprises",
        "Notes": "SKU: FDP-AUTONOMOUS-SOLOPRENEUR | Delivery: https://github.com/brettanthonysjoberg179-lab/autonomous-solopreneur | ABN: 63590716023",
        "Status": "Published",
        "Price": 47.00,
        "Product Type": "Ebook & Masterclass Bundle",
        "Category": "AI & Agentic Automation",
        "Description": "The definitive blueprint for solo creators and technical founders on how to architect, orchestrate, and monetize autonomous AI agent workforces.",
        "Publish Status": "LIVE"
    }
    
    r = requests.post(
        url,
        json={"fields": fields, "typecast": True},
        headers=headers,
        timeout=30
    )
    if r.status_code == 200:
        rec = r.json()
        print(f"[+] Successfully uploaded product to Airtable! Record ID: {rec.get('id')}")
    else:
        print(f"[!] Airtable sync error {r.status_code}: {r.text}")
