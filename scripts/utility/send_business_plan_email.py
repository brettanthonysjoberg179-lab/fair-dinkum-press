import json
import subprocess
import sys

payload = {
    "recipient_email": "brettanthonysjoberg179@gmail.com",
    "subject": "Fair Dinkum Publishing — Business Plan 2026-09-25 (Base A$5,615)",
    "body": (
        "Hi Brett,\n\n"
        "Here is the finalized Fair Dinkum Publishing Business Plan (dated 2026-09-25).\n\n"
        "--- EXECUTIVE SUMMARY & FINANCIAL PROJECTIONS ---\n"
        "• Conservative Model: A$1,482 / yr\n"
        "• Base Model (Planning Case): A$5,615 / yr\n"
        "• Optimistic Model: A$20,064 / yr\n\n"
        "Asset Inventory:\n"
        "- Tier 1 LIVE: 5 SKUs (A$181 basket)\n"
        "- Tier 2 Local-Live / Tier 3 Built: 14 PDFs (US$498 value)\n"
        "- Tier 4 Pipeline: MCP & Agent automation suites\n\n"
        "Attached: business-plan-2026-09-25.pdf (6 pages)\n\n"
        "Best regards,\nFair Dinkum Autonomous Orchestrator"
    )
}

payload_path = "outputs/email_payload.json"
import pathlib
pathlib.Path(payload_path).parent.mkdir(parents=True, exist_ok=True)
pathlib.Path(payload_path).write_text(json.dumps(payload))

cmd = [
    "composio", "execute", "GMAIL_SEND_EMAIL",
    "--file", "digital_product_workforce/outputs/business-plan-2026-09-25.pdf",
    "-d", f"@{payload_path}"
]

print("Sending business plan email via Composio...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print(res.stderr, file=sys.stderr)
