#!/usr/bin/env python3
"""
Composio Gmail B2B Outreach Agent
===================================
Automates sending tailored B2B outreach emails via Composio Gmail tools
for "The AU AI Compliance Playbook" and 1-on-1 AI Compliance Audits.

Usage:
    python composio_outreach_agent.py --dry-run
    python composio_outreach_agent.py --send
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

COMPOSIO_CLI = "/home/brettanthonysjoberg179/.local/bin/composio"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Curated B2B Prospect List for AU AI Compliance Outreach
PROSPECTS = [
    {
        "name": "Sydney Real Estate Group",
        "email": "sydney.realestate.lead@example.com",
        "niche": "Real Estate",
        "city": "Sydney"
    },
    {
        "name": "Melbourne Medical & Dental Clinic",
        "email": "melbourne.medical.lead@example.com",
        "niche": "Healthcare",
        "city": "Melbourne"
    },
    {
        "name": "Brisbane Financial & Accounting Partners",
        "email": "brisbane.finance.lead@example.com",
        "niche": "Finance",
        "city": "Brisbane"
    }
]

EMAIL_SUBJECT = "Is your AI usage compliant with the Privacy Act 1988 (APP 1.7)?"

EMAIL_TEMPLATE = """Hi {name} Team,

With the OAIC actively reviewing automated decision-making and AI tools under the Privacy Act 1988, many Australian businesses operating in {city} are unknowingly exposed to compliance risks regarding consumer-grade AI tools.

We’ve just released **The AU AI Compliance Playbook**, designed specifically for Australian businesses navigating AI adoption.

- **Option 1 (DIY Playbook):** Instant access to the 207-page guide + templates ($149 AUD) -> https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u
- **Option 2 (DFY Audit):** Book a 1-on-1 AI Compliance Audit & Report ($1,500 AUD) -> https://calendly.com/brett-sjoberg/ai-compliance-audit

Would you like a complimentary 5-minute AI risk assessment for {name}?

Best regards,

Brett Anthony Sjoberg  
Fair Dinkum Publishing & AI Advisory  
"""

def execute_composio(tool_slug: str, params: dict) -> dict:
    cmd = [COMPOSIO_CLI, "execute", tool_slug, "-d", json.dumps(params)]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        raise RuntimeError(f"Composio failed: {res.stderr or res.stdout}")
    try:
        out = res.stdout
        start = out.find('{')
        end = out.rfind('}')
        if start != -1 and end != -1:
            return json.loads(out[start:end+1])
        return {"raw": out}
    except Exception as e:
        return {"error": str(e), "raw": res.stdout}

def run_outreach(dry_run: bool = True):
    print(f"🚀 Composio Gmail Outreach Agent starting (dry_run={dry_run})...")
    
    for p in PROSPECTS:
        body = EMAIL_TEMPLATE.format(name=p["name"], city=p["city"])
        print(f"\nTarget: {p['name']} ({p['email']}) | Niche: {p['niche']}")
        print(f"Subject: {EMAIL_SUBJECT}")
        
        if dry_run:
            print("  [DRY RUN] Email body preview:")
            print("-" * 40)
            print(body[:300] + "...\n[TRUNCATED]")
            print("-" * 40)
        else:
            print("  Sending email via Composio GMAIL_SEND_EMAIL...")
            try:
                res = execute_composio("GMAIL_SEND_EMAIL", {
                    "recipient_email": p["email"],
                    "subject": EMAIL_SUBJECT,
                    "body": body
                })
                print(f"  Successfully sent! Response: {res}")
            except Exception as e:
                print(f"  Error sending email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Composio Gmail B2B Outreach Agent")
    parser.add_argument("--send", action="store_true", help="Actually send emails via Composio (default is dry-run)")
    args = parser.parse_args()
    
    run_outreach(dry_run=not args.send)
