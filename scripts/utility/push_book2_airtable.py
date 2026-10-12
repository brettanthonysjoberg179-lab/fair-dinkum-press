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

if not api_key:
    print("[!] AIRTABLE_API_KEY not found")
else:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    url = f"{API_ROOT}/{base_id}/{table_id}"
    fields = {
        "Name": "Programmatic Dominance: Scaling Automated SEO & High-Velocity Content Networks",
        "Notes": "SKU: FDP-PROGRAMMATIC-DOMINANCE | Delivery: https://github.com/brettanthonysjoberg179-lab/programmatic-dominance | ABN: 63590716023",
        "Status": "Published",
        "Price": 47.00,
        "Product Type": "Ebook & Masterclass Bundle",
        "Category": "Programmatic SEO & Content",
        "Description": "The sequel masterclass on scaling automated search engine optimization and high-velocity content networks using AI agent swarms.",
        "Publish Status": "LIVE"
    }
    r = requests.post(url, json={"fields": fields, "typecast": True}, headers=headers, timeout=30)
    if r.status_code == 200:
        rec = r.json()
        print(f"[+] Successfully pushed Book 2 to Airtable! Record ID: {rec.get('id')}")
    else:
        print(f"[!] Airtable sync error {r.status_code}: {r.text}")
