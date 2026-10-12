#!/usr/bin/env python3
"""
Gmail Business Outreach Marketing & Growth Agent
Identity: opal-vista-wombat@agents.composio.io
Prospects target creators/founders and sends personalized masterclass promotion emails.
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

print("Initializing Gmail Business Outreach & Growth Agent...")
print(f"Agent Identity: opal-vista-wombat@agents.composio.io")

# Sample target prospects for outreach
PROSPECTS = [
    {"name": "Alex Turner", "email": "alex.turner@solopreneurdev.io", "niche": "SaaS Founder"},
    {"name": "Sarah Jenkins", "email": "sarah@jenkinsconsulting.com", "niche": "B2B Consultant"},
    {"name": "Liam O'Connor", "email": "liam@aipublishinghub.com", "niche": "Digital Creator"}
]

def generate_outreach_email(prospect):
    subject = f"Scaling {prospect['name']}'s agency with 24/7 AI agent swarms 🚀"
    body = f"""Hi {prospect['name']},

I noticed your work in the {prospect['niche']} space and love what you're building. 

Many founders in your position hit a hard ceiling because they spend hours manually prompting LLMs instead of orchestrating automated workflows. 

We just published 'The Autonomous Solopreneur: Building & Scaling Multi-Agent AI Enterprises' alongside our Enterprise Masterclass Bundle—a complete operational blueprint covering role-specialized agent swarms, tiered memory RAGs, programmatic SEO, and headless Gumroad/Stripe distribution.

Would you be open to taking a complimentary look at the masterclass? 

Best regards,
Brett Sjoberg
Chief Architect, Fair Dinkum Publishing
https://github.com/brettanthonysjoberg179-lab/autonomous-solopreneur
"""
    return subject, body

def send_outreach(prospect, dry_run=True):
    subject, body = generate_outreach_email(prospect)
    print(f"\n[Outreach Target: {prospect['name']} <{prospect['email']}>]")
    print(f"Subject: {subject}")
    print(f"Body Preview:\n{body[:300]}...\n")
    
    if dry_run:
        print("[DRY RUN] Email logged safely. Set dry_run=False to execute live send via Gmail.")
        return True
    
    # Send via Composio Gmail tool
    payload = {
        "recipient_email": prospect['email'],
        "subject": subject,
        "body": body,
        "user_id": "me"
    }
    cmd = ["composio", "execute", "GMAIL_SEND_EMAIL", "-d", json.dumps(payload)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[+] Successfully sent live outreach email to {prospect['email']}!")
        return True
    else:
        print(f"[!] Send failed: {res.stderr}")
        return False

if __name__ == "__main__":
    print(f"Loaded {len(PROSPECTS)} growth prospects.")
    for p in PROSPECTS:
        send_outreach(p, dry_run=True)
