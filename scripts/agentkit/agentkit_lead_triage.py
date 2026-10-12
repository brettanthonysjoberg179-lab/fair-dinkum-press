#!/usr/bin/env python3
"""
AgentKit Shop Template: Inbound Lead Triage & Gmail Reply Draft Agent
===================================================================
Fetches unread inbound emails via Composio Gmail tools, classifies lead intent,
generates a tailored reply draft, creates the draft in Gmail, and logs results.

Usage:
    python agentkit_lead_triage.py --dry-run
    python agentkit_lead_triage.py --live --max 5
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

COMPOSIO_CLI = "/home/brettanthonysjoberg179/.local/bin/composio"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

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

def classify_and_draft(sender: str, subject: str, snippet: str) -> dict:
    text = f"{subject} {snippet}".lower()
    
    if "pricing" in text or "cost" in text or "buy" in text or "enterprise" in text or "pack" in text:
        category = "Hot Sales / Pricing"
        reply_body = f"Hi there,\n\nThanks for reaching out regarding AgentKit Shop pricing and workflow packs. Whether you're looking for our $19 single templates or the $149 all-access bundle, you can get started instantly here: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u\n\nWould you like a quick demo or recommendations for your specific stack?\n\nBest,\nAgentKit Shop Autonomous Triage Agent"
    elif "support" in text or "error" in text or "bug" in text or "help" in text:
        category = "Technical Support"
        reply_body = f"Hi there,\n\nWe received your support request regarding AgentKit Shop. Our automated CI tests and engineering team are reviewing your query. For immediate troubleshooting, check our repo docs or reply with your error logs.\n\nBest,\nAgentKit Shop Support Agent"
    elif "affiliate" in text or "partner" in text or "collaborate" in text:
        category = "Affiliate / Partnership"
        reply_body = f"Hi there,\n\nThanks for your interest in partnering with AgentKit Shop! We offer a 30% affiliate commission via Gumroad. Let's discuss collaboration details.\n\nBest,\nAgentKit Shop Partnerships Team"
    else:
        category = "General Inquiry"
        reply_body = f"Hi there,\n\nThanks for reaching out to AgentKit Shop! We build production-ready AI agent workflow packs for indie devs and small businesses. How can we help you accelerate your automation stack today?\n\nBest,\nAgentKit Shop Team"
        
    return {
        "category": category,
        "reply_subject": f"Re: {subject}",
        "reply_body": reply_body
    }

def run_triage(dry_run: bool = True, max_results: int = 3):
    print(f"🚀 AgentKit Inbound Lead Triage Agent starting (dry_run={dry_run}, max_results={max_results})...")
    
    # 1. Fetch unread emails
    try:
        fetch_res = execute_composio("GMAIL_FETCH_EMAILS", {
            "query": "is:unread",
            "max_results": max_results,
            "user_id": "me"
        })
    except Exception as e:
        print(f"⚠️ Failed to fetch live emails via Composio (may need re-auth or no unread mail): {e}")
        print("💡 Falling back to simulated inbound lead for demonstration...")
        fetch_res = {
            "messages": [
                {
                    "id": "simulated_lead_001",
                    "threadId": "thread_sim_001",
                    "snippet": "Hi, I'm interested in enterprise pricing and custom packs for my real estate agency.",
                    "payload": {
                        "headers": [
                            {"name": "Subject", "value": "Enterprise pricing & real estate agent packs"},
                            {"name": "From", "value": "buyer@sydneyrealestate.example.com"}
                        ]
                    }
                }
            ]
        }

    messages = fetch_res.get("messages", [])
    if not messages and isinstance(fetch_res.get("raw"), str):
        # try parsing raw output if structured messages not found
        messages = [{"id": "simulated_lead_001", "snippet": fetch_res.get("raw")[:200], "payload": {"headers": [{"name": "Subject", "value": "Inquiry"}, {"name": "From", "value": "lead@example.com"}]}}]

    print(f"📥 Found {len(messages)} message(s) to triage.")
    
    results = []
    for msg in messages:
        msg_id = msg.get("id", "unknown")
        snippet = msg.get("snippet", "")
        headers = msg.get("payload", {}).get("headers", [])
        
        subject = "Inquiry"
        sender = "unknown@example.com"
        for h in headers:
            if h.get("name") == "Subject":
                subject = h.get("value")
            elif h.get("name") == "From":
                sender = h.get("value")
                
        print(f"\n--- Processing Message ID: {msg_id} ---")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Snippet: {snippet[:120]}...")
        
        triage = classify_and_draft(sender, subject, snippet)
        print(f"🏷️ Category: {triage['category']}")
        print(f"✉️ Draft Subject: {triage['reply_subject']}")
        
        action_status = "dry_run"
        if not dry_run and not msg_id.startswith("simulated"):
            print("  Creating draft reply in Gmail via Composio GMAIL_CREATE_EMAIL_DRAFT...")
            try:
                draft_res = execute_composio("GMAIL_CREATE_EMAIL_DRAFT", {
                    "recipient_email": sender,
                    "subject": triage["reply_subject"],
                    "body": triage["reply_body"]
                })
                print(f"  Draft created successfully: {draft_res}")
                action_status = "draft_created"
            except Exception as e:
                print(f"  Failed to create draft: {e}")
                action_status = f"error: {str(e)}"
        else:
            print("  [DRY RUN] Would create Gmail draft and mark email as read.")
            
        results.append({
            "message_id": msg_id,
            "sender": sender,
            "subject": subject,
            "category": triage["category"],
            "action_status": action_status,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    report_path = LOG_DIR / "agentkit_lead_triage_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Triage report saved to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgentKit Inbound Lead Triage Agent")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run mode without mutating Gmail")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Execute live actions via Composio")
    parser.add_argument("--max", type=int, default=3, help="Max results to fetch")
    args = parser.parse_args()
    
    run_triage(dry_run=args.dry_run, max_results=args.max)
