#!/usr/bin/env python3
"""
AgentKit Shop: Webhook Fulfillment Test
======================================
Simulates a Gumroad or Stripe purchase webhook call to `webhook_server.py`
for AgentKit Shop products, verifying the backend automation loop.

Usage:
    python agentkit_test_webhook.py
"""

import json
import urllib.request
import urllib.error

SERVER_URL = "http://localhost:8000/webhook/gumroad"

MOCK_GUMROAD_PAYLOAD = {
    "product_name": "AgentKit Small Business Automation Pack",
    "price": 5900,
    "email": "buyer@indiedev.example.com",
    "sale_id": "SALE-AGENTKIT-2026-001",
    "url_params": {}
}

def test_webhook():
    print(f"🚀 Testing AgentKit webhook fulfillment against {SERVER_URL}...")
    req = urllib.request.Request(
        SERVER_URL,
        data=json.dumps(MOCK_GUMROAD_PAYLOAD).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
            print(f"✅ Webhook response status: {resp.status}")
            print(f"📦 Response body: {body}")
    except urllib.error.URLError as e:
        print(f"⚠️ Webhook server not running locally on port 8000 ({e}).")
        print("💡 Start the webhook server with: python webhook_server.py")
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")

if __name__ == "__main__":
    test_webhook()
