#!/usr/bin/env python3
"""Generate cover art for Book 2: 'Programmatic Dominance'."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#0F172A")
draw = ImageDraw.Draw(img)

for i in range(H):
    t = i / H
    r = int(245 + (16 - 245) * t)
    g = int(158 + (185 - 158) * t)
    b = int(11 + (129 - 11) * t)
    draw.line([(0, i), (W, i)], fill=(r, g, b))

def get_font(size):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

font_title = get_font(48)
font_sub = get_font(26)
font_badge = get_font(20)

draw.rectangle([80, 80, 360, 130], fill="#1E293B", outline="#F59E0B", width=2)
draw.text((100, 93), "BOOK 2 · SEQUEL", fill="#F59E0B", font=font_badge)

draw.text((80, 160), "PROGRAMMATIC DOMINANCE", fill="#FFFFFF", font=font_title)
draw.text((80, 230), "Scaling Automated SEO & High-Velocity Content Networks", fill="#F8FAFC", font=font_sub)

draw.rounded_rectangle([80, 460, 520, 540], radius=12, fill="#0F172A", outline="#F59E0B", width=2)
draw.text((110, 482), "pSEO Matrix Architecture • Traffic Scaling", fill="#FBBF24", font=font_sub)

os.makedirs("outputs", exist_ok=True)
img.save("outputs/programmatic_dominance_cover.png")
print("Book 2 cover generated: outputs/programmatic_dominance_cover.png")
