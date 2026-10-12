#!/usr/bin/env python3
"""Generate bold gradient covers for all 14 Gumroad products."""
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Product data
products = [
    {"id": "04GxzCtpL3JAqYdwx8zatg==", "name": "Email Marketing Swipe File: 50 Subject Lines, 20 Sequences, 10 Flows", "price": "A$27", "cat": "marketing"},
    {"id": "G2ioC8YmZjNOvtKOur7niQ==", "name": "Digital Nomad Starter Kit: Work Remotely From Anywhere", "price": "A$35", "cat": "productivity"},
    {"id": "UcCPlrS30VtNLXnb4vcXaA==", "name": "Notion Second Brain: PARA Method Template", "price": "A$39", "cat": "productivity"},
    {"id": "wQ5hvwF0rP8mxcIiy7eWAw==", "name": "Freelance Proposal Template That Wins Projects", "price": "A$29", "cat": "freelance"},
    {"id": "Mg9Bcungn-ZICAlY6014yw==", "name": "Digital Wellness Planner: 30-Day Anxiety Reset", "price": "A$19", "cat": "wellness"},
    {"id": "TjVI8pxWvDygiuPMfP5A-w==", "name": "Content Creator Starter Kit: Scripts, Captions & UGC Prompts", "price": "A$37", "cat": "content"},
    {"id": "CAV7nDn4E3FjrF_dnqaYgQ==", "name": "ATS Resume Template Pack: 5 Clean Formats + Cover Letters", "price": "A$25", "cat": "career"},
    {"id": "MBiCUk1vuAgQtVZRXuRIuA==", "name": "Freelance Notion Dashboard: Clients, Invoicing, Projects & Taxes", "price": "A$39", "cat": "freelance"},
    {"id": "R4kxz_YNWWn_DeiqW1y-3w==", "name": "AI Prompt Pack for Real Estate Agents: 50 Niche-Specific Prompts", "price": "A$19", "cat": "ai"},
    {"id": "lnd0IUXYn14ZlBOhFKGaiA==", "name": "GEO Keyword Injection Toolkit: 50 Templates to Get Cited by AI Search", "price": "$37", "cat": "ai"},
    {"id": "JcHK0wf-DRT8tq8pvcTzpA==", "name": "AI Agent Starter Kit", "price": "$57", "cat": "ai"},
    {"id": "FMG2VDvEs2pR_26bXaWgww==", "name": "Digital Product Launch Kit", "price": "$37", "cat": "marketing"},
    {"id": "gA2-oxFT7SDjPVX4cR0wyg==", "name": "100 AI Prompts for Content Creators", "price": "$47", "cat": "ai"},
    {"id": "zsiu1wV_4uqZo9Xue3MU2Q==", "name": "100 AI Prompts for Real Estate Agents", "price": "$29", "cat": "ai"},
]

# Vibrant gradient color schemes (modern SaaS)
gradients = {
    "ai":      (("#6366F1", "#8B5CF6"), ("#EC4899", "#F43F5E")),  # indigo→violet, pink→rose
    "marketing": (("#F59E0B", "#EF4444"), ("#3B82F6", "#6366F1")),  # amber→red, blue→indigo
    "productivity": (("#10B981", "#06B6D4"), ("#3B82F6", "#6366F1")),  # emerald→cyan, blue→indigo
    "freelance": (("#F97316", "#F59E0B"), ("#6366F1", "#8B5CF6")),  # orange→amber, indigo→violet
    "content": (("#EC4899", "#F43F5E"), ("#6366F1", "#8B5CF6")),  # pink→rose, indigo→violet
    "wellness": (("#14B8A6", "#06B6D4"), ("#6366F1", "#8B5CF6")),  # teal→cyan, indigo→violet
    "career": (("#64748B", "#475569"), ("#3B82F6", "#6366F1")),  # slate, blue→indigo
}

# Dimensions
W, H = 1200, 630

def draw_gradient(img, c1, c2, vertical=True):
    """Draw a linear gradient on the image."""
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    for i in range(H if vertical else W):
        t = i / (H if vertical else W)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        if vertical:
            draw.line([(0, i), (W, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, H)], fill=(r, g, b))

def get_font(size, bold=True):
    """Try to load a nice font, fall back to default."""
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/inter/Inter-Bold.otf",
        "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    # fallback
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def get_font_regular(size):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/inter/Inter-Regular.otf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def generate_cover(product, output_path):
    """Generate a single product cover."""
    cat = product["cat"]
    c1, c2 = gradients.get(cat, gradients["ai"])
    
    img = Image.new("RGB", (W, H))
    draw_gradient(img, c1[0], c1[1])
    
    # Overlay a subtle second gradient at angle
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for y in range(H):
        for x in range(0, W, 4):  # step for speed
            t = (x / W * 0.3 + y / H * 0.7)
            alpha = int(40 * t)
            overlay_draw.line([(x, y), (x+4, y)], fill=(255, 255, 255, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    
    draw = ImageDraw.Draw(img)
    
    # Draw decorative shapes
    overlay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    overlay2_draw = ImageDraw.Draw(overlay2)
    # Top-right circle
    overlay2_draw.ellipse([W-300, -150, W+100, 250], fill=(255, 255, 255, 30))
    # Bottom-left circle
    overlay2_draw.ellipse([-100, H-200, 200, H+100], fill=(255, 255, 255, 20))
    img = Image.alpha_composite(img.convert("RGBA"), overlay2).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Price tag (top-left)
    price_font = get_font(48, bold=True)
    price_text = product["price"]
    draw.text((60, 50), price_text, fill="white", font=price_font)
    
    # Main title
    title_font = get_font(72, bold=True)
    title_lines = wrap_text(product["name"], title_font, W - 120, draw)
    
    # Draw title centered-ish
    y_start = 180
    line_height = 85
    for i, line in enumerate(title_lines):
        draw.text((60, y_start + i * line_height), line, fill="white", font=title_font)
    
    # Category badge
    cat_font = get_font_regular(24)
    cat_text = cat.upper()
    bbox = draw.textbbox((0, 0), cat_text, font=cat_font)
    tw = bbox[2] - bbox[0]
    # Draw pill background
    pill_x, pill_y = 60, H - 100
    pill_w, pill_h = tw + 30, 44
    pill_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pill_draw = ImageDraw.Draw(pill_overlay)
    pill_draw.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h], radius=22, fill=(255, 255, 255, 60))
    img = Image.alpha_composite(img.convert("RGBA"), pill_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.text((pill_x + 15, pill_y + 8), cat_text, fill="white", font=cat_font)
    
    # "DIGITAL PRODUCT" label at bottom right
    label_font = get_font_regular(20)
    label = "DIGITAL PRODUCT"
    lbbox = draw.textbbox((0, 0), label, font=label_font)
    lw = lbbox[2] - lbbox[0]
    draw.text((W - lw - 60, H - 60), label, fill=(255, 255, 255, 180), font=label_font)
    
    img.save(output_path, "PNG", quality=95)
    return output_path

# Generate all covers
output_dir = "/home/brettanthonysjoberg179/gumroad-covers"
os.makedirs(output_dir, exist_ok=True)

results = []
for p in products:
    safe_name = p["name"].replace(" ", "-").replace("/", "-").replace(":", "").replace("?", "")[:50]
    filename = f"{p['id'][:8]}_{safe_name}.png"
    path = os.path.join(output_dir, filename)
    generate_cover(p, path)
    results.append({"id": p["id"], "name": p["name"], "path": path})
    print(f"✓ {p['name'][:40]}... → {filename}")

print(f"\nDone! {len(results)} covers in {output_dir}")
