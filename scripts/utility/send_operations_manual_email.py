import json
import subprocess
import sys
import os

payload = {
    "recipient_email": "brettanthonysjoberg179@gmail.com",
    "subject": "Fair Dinkum Publishing & AI Advisory — Business Operations Manual & Agent Architecture PDF Booklet",
    "body": (
        "Hi Brett,\n\n"
        "Attached is your finalized Business Operations Manual & Autonomous Agent Architecture PDF booklet for Fair Dinkum Publishing & AI Advisory.\n\n"
        "--- HIGHLIGHTS ---\n"
        "• Corporate Governance & Privacy Act APP 1.7 Compliance Rails\n"
        "• Product Value Ladder ($29 micro-guides to $1,500 DFY audits)\n"
        "• Cloudflare Edge Infrastructure (Workers, R2 storage, D1 SQLite database, Zero Trust Access)\n"
        "• Autonomous Agent Workforce & Tooling Sequences (Composio, Gmail, ClickSend SMS review flywheels)\n"
        "• Standard Operating Procedures (SOP-001 to SOP-003)\n\n"
        "Attached: fair_dinkum_business_operations_manual.pdf\n\n"
        "Best regards,\nFair Dinkum Autonomous Orchestrator"
    )
}

payload_path = "outputs/manual_email_payload.json"
os.makedirs("outputs", exist_ok=True)
with open(payload_path, "w") as f:
    json.dump(payload, f)

cmd = [
    "composio", "execute", "GMAIL_SEND_EMAIL",
    "--file", "outputs/fair_dinkum_business_operations_manual.pdf",
    "-d", f"@{payload_path}"
]

print("Sending Business Operations Manual PDF via Composio GMAIL_SEND_EMAIL...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)
