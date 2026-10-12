#!/usr/bin/env python3
"""
Real-Time Webhook Fulfillment Server (FastAPI)
Handles Gumroad and Stripe purchase webhooks, logs sales to Airtable, and triggers automated fulfillment.
"""

from fastapi import FastAPI, Request, HTTPException
import os
import requests

app = FastAPI(title="Fair Dinkum Webhook Fulfillment Server", version="1.1.0")

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

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "webhook-fulfillment-server", "version": "1.1.0"}

@app.post("/webhook/gumroad")
async def gumroad_webhook(request: Request):
    try:
        data = await request.json()
        print(f"[+] Received Gumroad Webhook: {data.get('product_name', 'Unknown Product')} - ${data.get('price', 0)/100.0}")
        
        # Log to Airtable
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID") or "appqqwluJEP7553HY"
        table_id = os.getenv("AIRTABLE_TABLE_ID") or "tblYavj3sIPsQeJcS"
        
        if api_key:
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            fields = {
                "Name": f"Sale: {data.get('product_name', 'Digital Product')}",
                "Notes": f"Customer: {data.get('email', 'N/A')} | Sale ID: {data.get('sale_id', 'N/A')}",
                "Status": "Sold",
                "Price": data.get("price", 0) / 100.0,
                "Product Type": "Sale",
                "Publish Status": "LIVE"
            }
            requests.post(f"https://api.airtable.com/v0/{base_id}/{table_id}", json={"fields": fields}, headers=headers, timeout=10)
            
        return {"status": "success", "message": "Gumroad webhook processed and logged."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    try:
        data = await request.json()
        print(f"[+] Received Stripe Webhook event: {data.get('type', 'unknown')}")
        return {"status": "success", "message": "Stripe webhook processed."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
