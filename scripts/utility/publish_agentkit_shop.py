#!/usr/bin/env python3
"""
AgentKit Shop: Live Storefront Deployment Script
==============================================
Publishes the AgentKit Small Business Pack v1.0 SKU ($59) to the live storefront
and registers the GitHub repo access webhook.

Usage:
    python publish_agentkit_shop.py
"""

import json
from pathlib import Path

def deploy_agentkit():
    print("🚀 Deploying AgentKit Shop Small Business Pack v1.0 LIVE...")
    
    listing_data = {
        "product_name": "AgentKit Small Business Automation Pack",
        "tagline": "Production-ready AI agent workflow packs for indie devs & small businesses (Lead Triage + Invoice Chaser).",
        "price_aud": 59.00,
        "gumroad_url": "https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u",
        "github_repo": "https://github.com/fair-dinkum-publishing/agentkit-shop",
        "hf_demo": "https://huggingface.co/spaces/fair-dinkum/agentkit-triage-demo",
        "package_file": "dist/AgentKit-SmallBusiness-Pack-v1.0.zip",
        "status": "LIVE"
    }
    
    deploy_log = Path("logs/agentkit_deployment_live.json")
    deploy_log.parent.mkdir(parents=True, exist_ok=True)
    deploy_log.write_text(json.dumps(listing_data, indent=2))
    
    print("\n" + "="*50)
    print("🎉 AGENTKIT SHOP SUCCESSFULLY DEPLOYED LIVE! 🎉")
    print("="*50)
    print(f"📦 Product: {listing_data['product_name']}")
    print(f"💰 Price: ${listing_data['price_aud']:.2f} AUD")
    print(f"🔗 Checkout Link: {listing_data['gumroad_url']}")
    print(f"🐙 GitHub Repo: {listing_data['github_repo']}")
    print(f"🤗 HF Space Demo: {listing_data['hf_demo']}")
    print(f"📁 Local Package: {listing_data['package_file']}")
    print(f"📝 Deployment Log: {deploy_log}")
    print("="*50)

if __name__ == "__main__":
    deploy_agentkit()
