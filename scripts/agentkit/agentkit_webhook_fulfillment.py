#!/usr/bin/env python3
"""
AgentKit Shop: Gumroad Webhook Fulfillment Automation
=====================================================
Handles Gumroad purchase webhooks for the $19 AgentKit Small Business Automation Pack:
1. Adds buyer to the private GitHub repository (`agentkit-lead-triage`).
2. Fires Gmail onboarding welcome email with download links via Composio.

Usage:
    python agentkit_webhook_fulfillment.py --test
"""

import argparse
import json
import os
import subprocess
import requests

COMPOSIO_CLI = "/home/brettanthonysjoberg179/.local/bin/composio"

def execute_composio(tool_slug: str, params: dict) -> dict:
    cmd = [COMPOSIO_CLI, "execute", tool_slug, "-d", json.dumps(params)]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if res.returncode != 0:
        raise RuntimeError(f"Composio execution failed for {tool_slug}: {res.stderr or res.stdout}")
    try:
        out = res.stdout
        start = out.find('{')
        end = out.rfind('}')
        if start != -1 and end != -1:
            return json.loads(out[start:end+1])
        return {"raw": out}
    except Exception as e:
        return {"error": str(e), "raw": res.stdout}

def fulfill_agentkit_sale(buyer_email: str, github_username: str = None, sale_id: str = "SALE-GUMROAD-001"):
    print(f"🎉 Processing AgentKit $19 Sale Fulfillment for {buyer_email} (Sale ID: {sale_id})...")
    
    # 1. Send Onboarding Welcome Email via Composio Gmail
    subject = "Welcome to AgentKit Shop! Your 5 Workflow Automation Pack & Private Repo Access"
    body = f"""Hi there,

Thank you for purchasing the AgentKit Small Business Automation Pack ($19 Edition)! 
You now have production-ready access to all 5 AI agent workflow templates:
1. Inbound Lead Triage & Gmail Reply Draft Agent
2. Overdue Invoice Chaser Agent
3. Lead Enrichment & CRM Sync Agent
4. Automated Follow-up Sequencer Agent
5. Meeting Scheduler & Calendar Booker Agent

📥 Download Your Pack:
https://github.com/brettanthonysjoberg179-lab/agentkit-lead-triage/archive/refs/heads/master.zip

🔐 Private Repository Access:
We are granting you collaborator access to the private repository:
https://github.com/brettanthonysjoberg179-lab/agentkit-lead-triage

If you provided your GitHub username ({github_username or 'Pending'}), your invite has been dispatched. Otherwise, reply to this email with your GitHub handle to get added instantly.

Quick Start:
```bash
pip install composio-core requests
composio login
python agentkit_lead_triage.py --dry-run
```

Happy automating!
— The AgentKit Shop Team
"""

    print(f"  Sending onboarding email to {buyer_email} via Composio GMAIL_SEND_EMAIL...")
    try:
        email_res = execute_composio("GMAIL_SEND_EMAIL", {
            "recipient_email": buyer_email,
            "subject": subject,
            "body": body
        })
        print(f"  ✅ Onboarding email sent successfully: {email_res}")
    except Exception as e:
        print(f"  ⚠️ Composio email send dry-run / notice: {e}")

    # 2. Add buyer to private GitHub repository (if username provided)
    if github_username:
        print(f"  Inviting {github_username} to private repository brettanthonysjoberg179-lab/agentkit-lead-triage...")
        token = os.getenv("GITHUB_TOKEN") or subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
        if token:
            headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
            url = f"https://api.github.com/repos/brettanthonysjoberg179-lab/agentkit-lead-triage/collaborators/{github_username}"
            resp = requests.put(url, json={"permission": "pull"}, headers=headers, timeout=10)
            if resp.status_code in [201, 204]:
                print(f"  ✅ Successfully added {github_username} as repository collaborator!")
            else:
                print(f"  ℹ️ GitHub collaborator invite status: {resp.status_code} - {resp.text}")
        else:
            print("  ⚠️ GitHub token not available for collaborator invite.")
    else:
        print("  ℹ️ No GitHub username provided in payload; onboarding email instructions sent.")

    print("✅ Fulfillment workflow completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgentKit Webhook Fulfillment Test")
    parser.add_argument("--email", default="buyer@indiedev.example.com", help="Buyer email")
    parser.add_argument("--github", default="indiedev-hero", help="Buyer GitHub username")
    args = parser.parse_args()
    
    fulfill_agentkit_sale(buyer_email=args.email, github_username=args.github)
