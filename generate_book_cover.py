#!/usr/bin/env python3
"""Generate high-impact cover art for 'The Autonomous Solopreneur' under Fair Dinkum Publishing Agent Workflowz."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#0F172A")
draw = ImageDraw.Draw(img)

# Draw gradient background (Indigo to Violet / Modern AI theme)
for i in range(H):
    t = i / H
    r = int(15 + (139 - 15) * t)
    g = int(23 + (92 - 23) * t)
    b = int(42 + (246 - 42) * t)
    draw.line([(0, i), (W, i)], fill=(r, g, b))

def get_font(size, bold=True):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

font_title = get_font(52)
font_sub = get_font(28, bold=False)
font_badge = get_font(20)

# Badge
draw.rectangle([80, 80, 420, 130], fill="#4F46E5", outline=None)
draw.text((100, 93), "FAIR DINKUM PUBLISHING", fill="#FFFFFF", font=font_badge)

# Title
draw.text((80, 170), "THE AUTONOMOUS SOLOPRENEUR", fill="#FFFFFF", font=font_title)
draw.text((80, 240), "Building & Scaling Multi-Agent AI Enterprises", fill="#E2E8F0", font=font_sub)

# Features / Footer pill
draw.rounded_rectangle([80, 460, 520, 540], radius=12, fill="#1E293B", outline="#4F46E5", width=2)
draw.text((110, 482), "10 Complete Chapters • Multi-Agent Blueprints", fill="#38BDF8", font=font_sub)

os.makedirs("outputs", exist_ok=True)
img.save("outputs/autonomous_solopreneur_cover.png")
print("Cover generated successfully: outputs/autonomous_solopreneur_cover.png")
