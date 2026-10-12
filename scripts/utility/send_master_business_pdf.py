#!/usr/bin/env python3
"""Send Master Business Profile PDF via Gmail."""

import json
import subprocess
import sys
import os

payload = {
    "recipient_email": "brettanthonysjoberg179@gmail.com",
    "subject": "Fair Dinkum Publishing & AI Advisory — Master Business Profile PDF Booklet",
    "body": (
        "Hi Brett,\n\n"
        "Attached is your finalized Master Business Profile & Cloudflare Edge Architecture PDF booklet for Fair Dinkum Publishing & AI Advisory.\n\n"
        "--- HIGHLIGHTS ---\n"
        "• Tiered Value Ladder ($29 micro-products to $1,500 DFY audits)\n"
        "• Automated Agentic Workflows (Composio email & outreach agents)\n"
        "• Cloudflare Edge Integration (R2 storage, Workers webhooks, D1 database, Pages CDN, Zero Trust Access)\n\n"
        "Attached: fair_dinkum_master_business_profile.pdf\n\n"
        "Best regards,\nFair Dinkum Autonomous Orchestrator"
    )
}

payload_path = "outputs/master_email_payload.json"
os.makedirs("outputs", exist_ok=True)
with open(payload_path, "w") as f:
    json.dump(payload, f)

cmd = [
    "composio", "execute", "GMAIL_SEND_EMAIL",
    "--file", "outputs/fair_dinkum_master_business_profile.pdf",
    "-d", f"@{payload_path}"
]

print("Sending master business profile PDF via Composio GMAIL_SEND_EMAIL...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)
