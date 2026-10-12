#!/usr/bin/env python3
"""Package Autonomous Solopreneur assets for Gumroad upload."""
import zipfile
import os

files_to_zip = [
    ("outputs/the_autonomous_solopreneur.epub", "the_autonomous_solopreneur.epub"),
    ("outputs/autonomous_solopreneur_cover.png", "cover.png"),
    ("the_autonomous_solopreneur_manuscript.md", "manuscript.md"),
    ("fair_dinkum_publishing_sales_copy.md", "sales_copy.md")
]

zip_path = "outputs/autonomous_solopreneur_gumroad_package.zip"
os.makedirs("outputs", exist_ok=True)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for local_path, arc_name in files_to_zip:
        if os.path.exists(local_path):
            zf.write(local_path, arc_name)
            print(f"Added {local_path} as {arc_name}")
        else:
            print(f"Warning: {local_path} not found")

print(f"\nGumroad package created successfully: {zip_path}")
print(f"File size: {os.path.getsize(zip_path)} bytes")
