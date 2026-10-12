#!/usr/bin/env python3
"""
Unified Multi-Platform Social Syndication Agent (Live Mode)
Broadcasts product launches and masterclass teasers across Reddit, Telegram, Discord, and Facebook.
"""

import subprocess
import json

TITLE = "🚀 The Autonomous Solopreneur & Enterprise Masterclass Library is Live!"
MESSAGE = (
    "Stop prompting. Start orchestrating. Our complete library of masterclasses and books "
    "on building 24/7 autonomous AI agent workforces, programmatic SEO, and headless distribution is now live. "
    "Check out our private GitHub repos and Gumroad store today!"
)

def execute_reddit():
    print("[*] Broadcasting to Reddit (r/Entrepreneur)...")
    payload = {
        "subreddit": "Entrepreneur",
        "title": TITLE,
        "text": MESSAGE,
        "kind": "self",
        "flair_id": "c2f22a12-e1d8-11e3-a77b-12313b0a74a7"
    }
    cmd = ["composio", "execute", "REDDIT_CREATE_REDDIT_POST", "-d", json.dumps(payload)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout if res.returncode == 0 else f"Reddit error: {res.stderr}")

def execute_telegram():
    print("[*] Broadcasting to Telegram...")
    # Using TELEGRAM_SEND_MESSAGE (requires chat_id or channel)
    payload = {
        "chat_id": "@fairdinkum_publishing", # Or default active chat
        "text": f"{TITLE}\n\n{MESSAGE}"
    }
    cmd = ["composio", "execute", "TELEGRAM_SEND_MESSAGE", "-d", json.dumps(payload)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout if res.returncode == 0 else f"Telegram note: {res.stderr}")

if __name__ == "__main__":
    print("=== Omni-Syndicator Live Execution ===")
    execute_reddit()
    execute_telegram()
    print("[+] Live syndicator execution completed.")
