#!/usr/bin/env python3
"""Generate Gumroad listing thumbnails (600x315) from existing covers."""
import os
from PIL import Image

COVERS_DIR = "/home/brettanthonysjoberg179/gumroad-covers"
THUMB_DIR = "/home/brettanthonysjoberg179/gumroad-thumbs"
THUMB_SIZE = (600, 315)

os.makedirs(THUMB_DIR, exist_ok=True)

covers = sorted(f for f in os.listdir(COVERS_DIR) if f.endswith(".png"))
print(f"Generating {len(covers)} thumbnails at {THUMB_SIZE[0]}x{THUMB_SIZE[1]}...")

for name in covers:
    src = os.path.join(COVERS_DIR, name)
    dst = os.path.join(THUMB_DIR, name)
    img = Image.open(src)
    thumb = img.resize(THUMB_SIZE, Image.LANCZOS)
    thumb.save(dst, "PNG", optimize=True)
    size_kb = os.path.getsize(dst) // 1024
    print(f"  {name[:50]}... → {size_kb}KB")

print(f"\nDone! {len(covers)} thumbnails in {THUMB_DIR}")
