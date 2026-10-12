#!/usr/bin/env python3
"""Generate workbook cover art for 'The Autonomous Solopreneur Companion Workbook'."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#0F172A")
draw = ImageDraw.Draw(img)

for i in range(H):
    t = i / H
    r = int(16 + (30 - 16) * t)
    g = int(185 + (144 - 185) * t)
    b = int(129 + (255 - 129) * t)
    draw.line([(0, i), (W, i)], fill=(r, g, b))

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

font_title = get_font(46)
font_sub = get_font(26)
font_badge = get_font(20)

draw.rectangle([80, 80, 380, 130], fill="#059669")
draw.text((100, 93), "COMPANION WORKBOOK", fill="#FFFFFF", font=font_badge)

draw.text((80, 160), "THE AUTONOMOUS SOLOPRENEUR", fill="#FFFFFF", font=font_title)
draw.text((80, 230), "Implementation Guide & Operational Checklists", fill="#E2E8F0", font=font_sub)

draw.rounded_rectangle([80, 460, 480, 540], radius=12, fill="#0F172A", outline="#10B981", width=2)
draw.text((110, 482), "Actionable Frameworks & Templates", fill="#34D399", font=font_sub)

os.makedirs("outputs", exist_ok=True)
img.save("outputs/workbook_cover.png")
print("Workbook cover generated: outputs/workbook_cover.png")
