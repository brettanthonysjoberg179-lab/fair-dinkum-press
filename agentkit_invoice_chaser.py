#!/usr/bin/env python3
"""
AgentKit Shop Template: Overdue Invoice Chaser Agent
===================================================
Checks for overdue invoices or unpaid client balances and automates polite follow-up
emails via Composio Gmail and Stripe payment link generation.

Usage:
    python agentkit_invoice_chaser.py --dry-run
    python agentkit_invoice_chaser.py --live
"""

import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime

COMPOSIO_CLI = "/home/brettanthonysjoberg179/.local/bin/composio"
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

MOCK_INVOICES = [
    {
        "client_name": "Apex Digital Agency",
        "client_email": "billing@apexdigital.example.com",
        "invoice_id": "INV-2026-042",
        "amount_due_aud": 1500.00,
        "due_date": "2026-09-28",
        "payment_link": "https://buy.stripe.com/test_invoice_apex"
    },
    {
        "client_name": "Melbourne Consultancy Group",
        "client_email": "accounts@melbourneconsult.example.com",
        "invoice_id": "INV-2026-048",
        "amount_due_aud": 3200.00,
        "due_date": "2026-10-01",
        "payment_link": "https://buy.stripe.com/test_invoice_melb"
    }
]

def run_invoice_chaser(dry_run: bool = True):
    print(f"🚀 AgentKit Invoice Chaser Agent starting (dry_run={dry_run})...")
    
    results = []
    for inv in MOCK_INVOICES:
        print(f"\nClient: {inv['client_name']} ({inv['client_email']})")
        print(f"Invoice: {inv['invoice_id']} | Amount: ${inv['amount_due_aud']:.2f} AUD | Due: {inv['due_date']}")
        
        subject = f"Friendly Reminder: Overdue Invoice {inv['invoice_id']} for ${inv['amount_due_aud']:.2f} AUD"
        body = f"""Hi {inv['client_name']} Accounts Team,

This is a friendly reminder that invoice {inv['invoice_id']} for ${inv['amount_due_aud']:.2f} AUD was due on {inv['due_date']} and remains unpaid.

You can securely settle this balance instantly via Stripe:
{inv['payment_link']}

If you've already made this payment, please disregard this notice. Thank you for your prompt attention!

Best regards,
AgentKit Shop Automated Billing Agent
"""
        
        action_status = "dry_run"
        if not dry_run:
            print("  Sending payment reminder via Composio GMAIL_SEND_EMAIL...")
            try:
                cmd = [
                    COMPOSIO_CLI, "execute", "GMAIL_SEND_EMAIL",
                    "-d", json.dumps({
                        "recipient_email": inv["client_email"],
                        "subject": subject,
                        "body": body
                    })
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if res.returncode == 0:
                    print("  Successfully sent reminder!")
                    action_status = "sent"
                else:
                    print(f"  Failed: {res.stderr or res.stdout}")
                    action_status = "error"
            except Exception as e:
                print(f"  Exception: {e}")
                action_status = f"error: {e}"
        else:
            print("  [DRY RUN] Would send payment reminder email.")
            
        results.append({
            "client_name": inv["client_name"],
            "invoice_id": inv["invoice_id"],
            "amount": inv["amount_due_aud"],
            "action_status": action_status,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    report_path = LOG_DIR / "agentkit_invoice_chaser_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Invoice chaser report saved to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgentKit Invoice Chaser Agent")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--live", action="store_false", dest="dry_run")
    args = parser.parse_args()
    run_invoice_chaser(dry_run=args.dry_run)
