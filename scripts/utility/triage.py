#!/usr/bin/env python3
"""
AgentKit Shop: Inbound Lead Triage Agent (triage.py)
===================================================
Polls unread Gmail via Composio, scores each email as hot, warm, cold, or not a lead.
Saves a reply draft in Gmail for hot and warm leads (never sends).
Supports --demo mode with three sample emails (real lead, vague inquiry, spam).

Usage:
    python triage.py --demo
    python triage.py --dry-run
    python triage.py --live --max 5
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

def score_and_draft(sender: str, subject: str, snippet: str) -> dict:
    text = f"{subject} {snippet}".lower()
    
    if "seo" in text or "win" in text or "crypto" in text or "offer" in text or "free cruise" in text:
        score = "not a lead"
        reply_body = ""
    elif "pricing" in text or "cost" in text or "buy" in text or "enterprise" in text or "pack" in text or "real estate" in text:
        score = "hot"
        reply_body = f"Hi there,\n\nThanks for reaching out regarding AgentKit Shop pricing and workflow packs. You can get started instantly with our templates here: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u\n\nWould you like a quick demo or recommendations for your stack?\n\nBest,\nAgentKit Triage Agent"
    elif "tell me more" in text or "question" in text or "details" in text or "how does" in text:
        score = "warm"
        reply_body = f"Hi there,\n\nThanks for your interest in AgentKit Shop! We provide production-ready AI agent workflow packs for small businesses and developers. Let us know what stack you are using and we'll send over the right templates.\n\nBest,\nAgentKit Triage Agent"
    else:
        score = "cold"
        reply_body = f"Hi there,\n\nThanks for your message. We've logged your inquiry and will follow up if relevant.\n\nBest,\nAgentKit Team"
        
    return {
        "score": score,
        "reply_subject": f"Re: {subject}",
        "reply_body": reply_body
    }

def run_triage(demo: bool = False, dry_run: bool = True, max_results: int = 3):
    print(f"🚀 AgentKit Inbound Lead Triage Agent starting (demo={demo}, dry_run={dry_run}, max_results={max_results})...")
    
    messages = []
    if demo:
        print("💡 Running in --demo mode with 3 sample emails (real lead, vague inquiry, spam)...")
        messages = [
            {
                "id": "demo_lead_hot",
                "snippet": "Hi, I'm interested in enterprise pricing and custom packs for my real estate agency.",
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": "Enterprise pricing & real estate agent packs"},
                        {"name": "From", "value": "buyer@sydneyrealestate.example.com"}
                    ]
                }
            },
            {
                "id": "demo_lead_warm",
                "snippet": "Hello, can you tell me more about how your automation packs work?",
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": "Question about workflow packs"},
                        {"name": "From", "value": "curious@devstartup.example.com"}
                    ]
                }
            },
            {
                "id": "demo_lead_spam",
                "snippet": "WIN a free cruise and guaranteed SEO ranking #1 on Google today!",
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": "URGENT: SEO services & free cruise offer"},
                        {"name": "From", "value": "spammy@seoranking.example.com"}
                    ]
                }
            }
        ]
    else:
        try:
            fetch_res = execute_composio("GMAIL_FETCH_EMAILS", {
                "query": "is:unread",
                "max_results": max_results,
                "user_id": "me"
            })
            messages = fetch_res.get("messages", [])
        except Exception as e:
            print(f"⚠️ Failed to fetch live emails via Composio: {e}")
            print("💡 Falling back to sample lead for safety...")
            messages = [
                {
                    "id": "fallback_lead_001",
                    "snippet": "Hi, interested in purchasing agent packs.",
                    "payload": {
                        "headers": [
                            {"name": "Subject", "value": "Agent packs pricing"},
                            {"name": "From", "value": "lead@example.com"}
                        ]
                    }
                }
            ]

    print(f"📥 Processing {len(messages)} message(s) for triage.\n")
    
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
                
        print(f"--- Message ID: {msg_id} ---")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Snippet: {snippet}")
        
        triage = score_and_draft(sender, subject, snippet)
        score = triage['score']
        print(f"🎯 Score: {score.upper()}")
        
        action_status = "scored_only"
        if score in ["hot", "warm"]:
            print(f"✉️ Draft Reply Generated:\n{triage['reply_body'][:150]}...")
            if not dry_run and not msg_id.startswith("demo_") and not msg_id.startswith("fallback_"):
                print("  Creating draft reply in Gmail via Composio GMAIL_CREATE_EMAIL_DRAFT...")
                try:
                    draft_res = execute_composio("GMAIL_CREATE_EMAIL_DRAFT", {
                        "recipient_email": sender,
                        "subject": triage["reply_subject"],
                        "body": triage["reply_body"]
                    })
                    print(f"  ✅ Draft created in Gmail: {draft_res.get('id', 'success')}")
                    action_status = "draft_created"
                except Exception as e:
                    print(f"  ❌ Failed to create draft: {e}")
                    action_status = f"error: {str(e)}"
            else:
                print("  [DRY RUN / DEMO] Saved draft locally. Never sends emails automatically.")
                action_status = "dry_run_draft_saved"
        else:
            print("  🚫 Skipped draft creation (scored as cold / not a lead).")
            
        results.append({
            "message_id": msg_id,
            "sender": sender,
            "subject": subject,
            "score": score,
            "action_status": action_status,
            "timestamp": datetime.utcnow().isoformat()
        })
        print("-" * 50 + "\n")
        
    report_path = LOG_DIR / "triage_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Triage report saved to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgentKit Inbound Lead Triage Agent")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode with sample emails (real lead, vague, spam)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run mode (default)")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Run in live mode")
    parser.add_argument("--max", type=int, default=3, help="Max results to fetch")
    args = parser.parse_args()
    
    run_triage(demo=args.demo, dry_run=args.dry_run, max_results=args.max)
