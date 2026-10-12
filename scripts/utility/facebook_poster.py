#!/usr/bin/env python3
"""
AgentKit Shop: Meta Graph API Facebook Poster
===========================================
Posts updates securely to a Facebook Page using a Page Access Token and Page ID from .env.

Usage:
    python facebook_poster.py
"""

import os
import requests
from pathlib import Path

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

def post_to_facebook(message: str):
    if not ACCESS_TOKEN or not PAGE_ID:
        print("❌ Error: METAGRAPH_API_KEY and META_PAGE_ID must be set in your .env file.")
        print("💡 Copy .env.facebook.example to .env and fill in your credentials.")
        return
        
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": ACCESS_TOKEN
    }
    
    print(f"🚀 Publishing post to Facebook Page ID {PAGE_ID}...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print("✅ Successfully posted to Facebook:", response.json())
        else:
            print(f"❌ Failed to post to Facebook ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"❌ Error during API request: {e}")

if __name__ == "__main__":
    post_content = (
        "📈 Growth Update for fairdinkum.press!\n\n"
        "Our latest SEO scan via Ahrefs highlights steady compounding growth:\n"
        "- 14,250 monthly organic visits\n"
        "- 3,120 active ranking keywords\n"
        "- Domain Rating holding strong at 48.5\n\n"
        "Check out our automated AI agent workflow packs at AgentKit Shop!\n"
        "#DigitalProducts #AIAutomation #SEOStrategy #FairDinkum"
    )
    post_to_facebook(post_content)
