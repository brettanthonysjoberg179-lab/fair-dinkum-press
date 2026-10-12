#!/usr/bin/env python3
"""
Sync local B2B prospects and sales records for Cloudflare D1 integration.
"""

import os
import json

def parse_prospects():
    prospects_file = "app_1_7_prospects.md"
    prospects = []
    if os.path.exists(prospects_file):
        with open(prospects_file, "r") as f:
            current_company = None
            current_email = None
            for line in f:
                line = line.strip()
                if line.startswith("## ") and "." in line:
                    if current_company:
                        prospects.append({
                            "company_name": current_company,
                            "email": current_email or "N/A",
                            "city": "Sydney",
                            "industry": "FinTech / Lending",
                            "status": "New"
                        })
                    # Extract company name after number and dot
                    parts = line.replace("## ", "").split(".", 1)
                    if len(parts) > 1:
                        current_company = parts[1].strip()
                        current_email = None
                elif line.startswith("- Email:"):
                    current_email = line.replace("- Email:", "").strip()
            
            if current_company:
                prospects.append({
                    "company_name": current_company,
                    "email": current_email or "N/A",
                    "city": "Sydney",
                    "industry": "FinTech / Lending",
                    "status": "New"
                })

    print(f"[+] Parsed {len(prospects)} prospects from {prospects_file}")
    return prospects

if __name__ == "__main__":
    print("Cloudflare D1 sync utility initialized.")
    prospects = parse_prospects()
    output_json = "outputs/d1_prospects_seed.json"
    os.makedirs("outputs", exist_ok=True)
    with open(output_json, "w") as f:
        json.dump(prospects, f, indent=2)
    print(f"[SUCCESS] Seed data written to {output_json}")
