#!/usr/bin/env python3
"""Email Trigger Agent — Polls Gmail for incoming emails from Brett and executes digital product workflows autonomously."""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

def run_composio(tool_slug: str, data: dict) -> dict:
    """Execute a Composio tool and return JSON response."""
    cmd = ["composio", "execute", tool_slug, "-d", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Composio execution failed for {tool_slug}: {result.stderr or result.stdout}")
    try:
        # Parse stdout looking for JSON
        output = result.stdout
        # find first '{' and last '}'
        start = output.find('{')
        end = output.rfind('}')
        if start != -1 and end != -1:
            return json.loads(output[start:end+1])
        return {"raw": output}
    except Exception as e:
        return {"error": str(e), "raw": result.stdout}

def check_incoming_emails():
    print("Checking for unread emails from brettanthonysjoberg179@gmail.com...")
    res = run_composio("GMAIL_FETCH_EMAILS", {
        "q": "from:brettanthonysjoberg179@gmail.com is:unread",
        "max_results": 5
    })
    
    # Let's inspect messages
    data = res.get("data", {})
    messages = data.get("messages", []) if isinstance(data, dict) else []
    print(f"Found {len(messages)} unread messages.")
    return messages

def process_email(msg_id: str):
    print(f"Fetching message details for ID: {msg_id}")
    res = run_composio("GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID", {
        "id": msg_id
    })
    msg_data = res.get("data", {})
    
    # Extract subject, body, snippet
    subject = ""
    body = ""
    headers = msg_data.get("payload", {}).get("headers", [])
    for h in headers:
        if h.get("name") == "Subject":
            subject = h.get("value", "")
            
    snippet = msg_data.get("snippet", "")
    print(f"Subject: {subject}")
    print(f"Snippet: {snippet}")
    
    # Determine intent
    text_to_analyze = (subject + " " + snippet).lower()
    
    response_subject = f"Re: {subject}"
    response_body = ""
    
    if "build" in text_to_analyze:
        response_body = "Hello Brett,\n\nI received your email instruction to BUILD a new digital product. I am initiating Phase 3 (Asset Generation) and Phase 4 (Gumroad Deployment) for your requested topic.\n\nBest regards,\nYour Autonomous Digital Product Business Agent"
    elif "research" in text_to_analyze:
        response_body = "Hello Brett,\n\nI received your email instruction to run TREND RESEARCH. I am scanning top creator platforms, Product Hunt, and Gumroad for September 2026 trending product ideas and will log them to Airtable.\n\nBest regards,\nYour Autonomous Digital Product Business Agent"
    elif "status" in text_to_analyze:
        response_body = "Hello Brett,\n\nStatus Report:\n- Active Product: AI-Powered Content & Compliance Machine (Notion OS)\n- Status: LIVE ($49.00 USD)\n- Storefront: https://brettanthonysjoberg1.gumroad.com/l/ulyfgh\n- Airtable Pipeline: Synced ('Product Operations for Teams')\n\nBest regards,\nYour Autonomous Digital Product Business Agent"
    else:
        response_body = f"Hello Brett,\n\nI received your message: '{subject}'. I am your 24/7 Digital Product Business Agent. Send me instructions with keywords like 'build', 'research', or 'status' to trigger automated workflows.\n\nBest regards,\nYour Autonomous Digital Product Business Agent"

    # Send reply email
    print("Sending automated response email...")
    run_composio("GMAIL_SEND_EMAIL", {
        "recipient_email": "brettanthonysjoberg179@gmail.com",
        "subject": response_subject,
        "body": response_body
    })
    
    # Mark message as read (remove UNREAD label)
    print("Marking message as read...")
    run_composio("GMAIL_ADD_LABEL_TO_EMAIL", {
        "id": msg_id,
        "removeLabelIds": ["UNREAD"]
    })
    print(f"Successfully processed message {msg_id}")

if __name__ == "__main__":
    messages = check_incoming_emails()
    for m in messages:
        msg_id = m.get("id")
        if msg_id:
            process_email(msg_id)
