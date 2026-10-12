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

if api_key:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    url = f"{API_ROOT}/{base_id}/{table_id}"
    fields = {
        "Name": "Enterprise AI Masterclass Bundle (The Autonomous Solopreneur + Programmatic Dominance)",
        "Notes": "SKU: FDP-MASTERCLASS-BUNDLE | Delivery: GitHub & Gumroad | ABN: 63590716023",
        "Status": "Published",
        "Price": 79.00,
        "Product Type": "Bundle",
        "Category": "AI & Agentic Automation",
        "Description": "Complete masterclass bundle combining The Autonomous Solopreneur and Programmatic Dominance at a 20% discount.",
        "Publish Status": "LIVE"
    }
    r = requests.post(url, json={"fields": fields, "typecast": True}, headers=headers, timeout=30)
    if r.status_code == 200:
        print(f"[+] Masterclass Bundle synced to Airtable! Record ID: {r.json().get('id')}")
    else:
        print(f"[!] Airtable sync error {r.status_code}: {r.text}")
