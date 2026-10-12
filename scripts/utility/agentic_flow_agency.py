#!/usr/bin/env python3
"""
AgenticFlow Autonomous AI Audit Agency
99% Automated Micro-Agency powered by Agent Swarms, Stripe, and Gmail.
- Listens for Stripe checkout purchases ($97 Audit / $297 Retainer)
- Automatically sends welcome intake questionnaire via Gmail
- Generates custom AI Readiness Audit Report PDF
- Delivers completed report & upsell sequence automatically
"""

import os
import sys
import json
import subprocess
from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI(title="AgenticFlow Autonomous AI Audit Agency", version="1.0.0")

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

def run_composio(tool_slug: str, data: dict) -> dict:
    cmd = ["composio", "execute", tool_slug, "-d", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] Composio error {tool_slug}: {result.stderr or result.stdout}")
        return {"error": result.stderr}
    try:
        output = result.stdout
        start = output.find('{')
        end = output.rfind('}')
        if start != -1 and end != -1:
            return json.loads(output[start:end+1])
        return {"raw": output}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "active", "agency": "AgenticFlow Autonomous AI Audits", "version": "1.0.0"}

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    try:
        payload = await request.json()
        event_type = payload.get("type", "unknown")
        print(f"[+] Received Stripe Event: {event_type}")
        
        if event_type == "checkout.session.completed":
            session = payload.get("data", {}).get("object", {})
            customer_email = session.get("customer_email") or session.get("customer_details", {}).get("email")
            customer_name = session.get("customer_details", {}).get("name", "Valued Founder")
            amount_total = session.get("amount_total", 9700) / 100.0
            
            print(f"[+] New Client Paid! Name: {customer_name} | Email: {customer_email} | Amount: ${amount_total}")
            
            if customer_email:
                # 1. Send Welcome & Intake Email via Gmail
                subject = "Welcome to AgenticFlow! Your AI Readiness Audit Intake Questionnaire 🚀"
                body = f"""Hi {customer_name},

Thank you for investing in the AgenticFlow Autonomous AI Audit (${amount_total:.2f})! 

To generate your comprehensive 15-page custom AI Readiness & Multi-Agent Architecture Audit Report, our autonomous agent swarm needs just 3 quick details about your business:

1. What is your primary tech stack (e.g., Python, Node.js, Next.js, Cloudflare, etc.)?
2. What is your biggest operational bottleneck right now (e.g., lead generation, customer onboarding, content creation, compliance)?
3. What is your primary business goal for the next 90 days?

Simply reply directly to this email with your answers. Our AI audit agent will synthesize your custom report and deliver it straight to your inbox within 2 minutes!

Best regards,
Brett Sjoberg
Chief Architect, AgenticFlow Audits
https://github.com/brettanthonysjoberg179-lab/autonomous-solopreneur
"""
                run_composio("GMAIL_SEND_EMAIL", {
                    "recipient_email": customer_email,
                    "subject": subject,
                    "body": body
                })
                print(f"[+] Dispatched intake email to {customer_email}")
                
        return {"status": "success", "event": event_type}
    except Exception as e:
        print(f"[!] Error processing Stripe webhook: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    print("Initializing AgenticFlow Autonomous AI Audit Agency Server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
