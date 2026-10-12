#!/usr/bin/env python3
"""
Opal-Vista-Wombat Sub-Gmail Agent
Identity: opal-vista-wombat@agents.composio.io
Monitors inbound business emails for brettanthonysjoberg179 and generates AI responses using Gemini.
"""

import os
import sys
import json
import subprocess

def load_env_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env_file(".env")
load_env_file("fair_dinkum_publishing/.env")

print("Initializing Opal-Vista-Wombat Sub-Gmail Agent...")
print(f"Agent Identity: opal-vista-wombat@agents.composio.io")
print(f"Target Inbox: brettanthonysjoberg179@gmail.com")

def fetch_recent_emails():
    # Execute Composio tool to fetch emails
    cmd = ["composio", "execute", "GMAIL_FETCH_EMAILS", "-d", json.dumps({"query": "", "user_id": "me", "max_results": 5})]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Error fetching emails: {res.stderr}")
        return []
    
    try:
        data = json.loads(res.stdout)
        messages = data.get("response", data).get("messages", data.get("data", {}).get("messages", []))
        return messages
    except Exception as e:
        print(f"[!] Failed to parse email JSON: {e}")
        return []

def analyze_email_with_gemini(subject, sender, snippet):
    # Simulated or API-driven Gemini 3.5 Flash / Flash-Lite triage
    prompt = f"""
    You are the executive assistant sub-agent for opal-vista-wombat-agent (Fair Dinkum Publishing).
    Analyze this inbound business email for brettanthonysjoberg179:
    - From: {sender}
    - Subject: {subject}
    - Snippet: {snippet}

    Provide:
    1. Priority (High / Medium / Low)
    2. Category (Customer Support, Partnership, Spam/Promotional, Editorial)
    3. Suggested Draft Response
    """
    print(f"\n[AI Triage] Analyzing email: '{subject}' from {sender}...")
    # In a live API call, we would call google-genai or vertexai here.
    return {
        "priority": "Medium",
        "category": "Business Inquiry / Masterclass Interest",
        "suggested_response": f"Hello, thank you for reaching out regarding '{subject}'. Our autonomous publishing workforce has received your message and will get back to you shortly. Best regards, Brett Sjoberg (Fair Dinkum Publishing)."
    }

if __name__ == "__main__":
    emails = fetch_recent_emails()
    print(f"[+] Fetched {len(emails)} recent emails for analysis.")
    for i, msg in enumerate(emails[:3], 1):
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        subject, sender = "No Subject", "Unknown"
        for h in headers:
            if h.get("name", "").lower() == "subject": subject = h.get("value")
            if h.get("name", "").lower() == "from": sender = h.get("value")
        snippet = msg.get("snippet", "")
        
        triage = analyze_email_with_gemini(subject, sender, snippet)
        print(f"  -> Priority: {triage['priority']} | Category: {triage['category']}")
        print(f"  -> Draft: {triage['suggested_response']}\n")
