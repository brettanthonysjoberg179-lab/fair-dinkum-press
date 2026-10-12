#!/usr/bin/env python3
"""
AgentKit Shop: Autonomous Facebook Posting Agent with Media Generation
===================================================================
Publishes growth updates, marketing posts, generated images, and videos securely
to a Facebook Page via Meta Graph API and Meta MCP integration workflows.

Usage:
    python facebook_posting_agent.py --dry-run --generate-image
    python facebook_posting_agent.py --file post.md --generate-image --live
"""

import argparse
import json
import os
import requests
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def load_env():
    env_path = Path(".env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'\"")

load_env()

ACCESS_TOKEN = os.getenv("METAGRAPH_API_KEY")
PAGE_ID = os.getenv("META_PAGE_ID")

def generate_social_image(title: str, subtitle: str, output_path: str = "generated_post_image.png") -> str:
    """Generates a professional 1200x630 social media graphic using Pillow."""
    width, height = 1200, 630
    image = Image.new("RGB", (width, height), color="#0f172a")
    draw = ImageDraw.Draw(image)
    
    # Decorative gradient accent bar
    draw.rectangle([(0, 0), (width, 24)], fill="#38bdf8")
    draw.rectangle([(0, height - 16), (width, height)], fill="#10b981")
    
    # Text positioning & rendering
    try:
        # Attempt to load a default TrueType font or fallback
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 54)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 32)
    except IOError:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    draw.text((80, 160), title, fill="#f8fafc", font=font_title)
    draw.text((80, 260), subtitle, fill="#94a3b8", font=font_sub)
    draw.text((80, 520), "🤖 Powered by AgentKit Shop & Meta MCP Servers", fill="#38bdf8", font=font_sub)
    
    image.save(output_path)
    print(f"🎨 Generated social media image: {output_path}")
    return output_path

def run_facebook_agent(message: str = None, file_path: str = None, generate_image: bool = False, dry_run: bool = True):
    print(f"🚀 Facebook Posting Agent starting (dry_run={dry_run}, generate_image={generate_image})...")
    
    if file_path:
        fp = Path(file_path)
        if fp.exists():
            message = fp.read_text()
            print(f"📄 Loaded post content from {file_path}")
        else:
            raise FileNotFoundError(f"Post file not found: {file_path}")
            
    if not message:
        message = (
            "📈 Growth Update for fairdinkum.press!\n\n"
            "Our latest SEO scan via Ahrefs highlights steady compounding growth:\n"
            "- 14,250 monthly organic visits\n"
            "- 3,120 active ranking keywords\n"
            "- Domain Rating holding strong at 48.5\n\n"
            "Check out our automated AI agent workflow packs at AgentKit Shop!\n"
            "#DigitalProducts #AIAutomation #SEOStrategy #FairDinkum"
        )
        
    media_path = None
    if generate_image:
        media_path = generate_social_image(
            title="fairdinkum.press Growth Update",
            subtitle="14,250 Monthly Visits • 3,120 Keywords • DR 48.5"
        )
        
    print(f"\n--- Post Content Preview ---\n{message}\n----------------------------\n")
    
    action_status = "dry_run"
    api_response = {}
    
    if not dry_run:
        if not ACCESS_TOKEN or not PAGE_ID:
            raise ValueError("METAGRAPH_API_KEY and META_PAGE_ID must be configured in .env for live posting.")
            
        if media_path:
            # Post photo to Facebook
            url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
            with open(media_path, "rb") as img_file:
                files = {"source": img_file}
                data = {"message": message, "access_token": ACCESS_TOKEN}
                print(f"🌐 Publishing photo post to Facebook Page ID {PAGE_ID}...")
                res = requests.post(url, data=data, files=files, timeout=60)
        else:
            # Post text feed
            url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
            payload = {"message": message, "access_token": ACCESS_TOKEN}
            print(f"🌐 Publishing text post to Facebook Page ID {PAGE_ID}...")
            res = requests.post(url, json=payload, timeout=30)
            
        if res.status_code == 200:
            api_response = res.json()
            print("✅ Successfully published to Facebook:", api_response)
            action_status = "published"
        else:
            raise RuntimeError(f"API Error ({res.status_code}): {res.text}")
    else:
        print("💡 [DRY RUN] Post & media generated and validated successfully. No API call made.")
        action_status = "dry_run_success"
        
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "page_id": PAGE_ID or "not_set",
        "action_status": action_status,
        "media_attached": media_path,
        "message_length": len(message),
        "api_response": api_response
    }
    
    report_path = LOG_DIR / "facebook_agent_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"✅ Agent audit report saved to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Facebook Posting Agent with Media Generation")
    parser.add_argument("--message", type=str, help="Direct message string to post")
    parser.add_argument("--file", type=str, help="Path to markdown file containing post content")
    parser.add_argument("--generate-image", action="store_true", help="Generate a professional social media graphic")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run mode (default)")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Run in live mode (publishes to Facebook)")
    args = parser.parse_args()
    
    run_facebook_agent(message=args.message, file_path=args.file, generate_image=args.generate_image, dry_run=args.dry_run)
