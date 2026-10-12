import zipfile
import os

files_to_zip = [
    ("outputs/programmatic_dominance.epub", "programmatic_dominance.epub"),
    ("outputs/programmatic_dominance_cover.png", "cover.png"),
    ("programmatic_dominance_manuscript.md", "manuscript.md")
]

zip_path = "outputs/programmatic_dominance_gumroad_package.zip"
os.makedirs("outputs", exist_ok=True)

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for local_path, arc_name in files_to_zip:
        if os.path.exists(local_path):
            zf.write(local_path, arc_name)
            print(f"Added {local_path} as {arc_name}")

print(f"Book 2 Gumroad package created: {zip_path}")
