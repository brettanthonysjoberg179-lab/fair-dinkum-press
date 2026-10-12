#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, '.')
from upload_to_sheets import upload_csv_to_sheet

files = [
    ("outputs/control_centre/MCP_Agents.csv", "MCP Agents Control Centre"),
    ("outputs/control_centre/Business_Metrics.csv", "Business Metrics Control Centre"),
    ("outputs/control_centre/Product_Inventory.csv", "Product Inventory Control Centre")
]

for csv_path, sheet_name in files:
    print(f"Uploading {csv_path} to Google Sheet '{sheet_name}'...")
    try:
        sheet_id, link = upload_csv_to_sheet(csv_path, sheet_name)
        print(f"Success! Sheet ID: {sheet_id}, Link: {link}\n")
    except Exception as e:
        print(f"Failed to upload {csv_path}: {e}\n")
