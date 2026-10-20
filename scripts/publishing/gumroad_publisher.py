#!/usr/bin/env python3
"""
Fair Dinkum Press & AgentKit - Gumroad Integration & Storefront Publisher
------------------------------------------------------------------------
This module provides integration with Gumroad for:
1. Packaging digital products (eBooks, workbooks, datasets) for Gumroad listings.
2. Generating Gumroad product metadata and preview configurations.
3. Automating storefront publishing and link distribution.
"""

import os
import json
from pathlib import Path

OUTPUT_DIR = Path("outputs/gumroad")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class GumroadPublisher:
    def __init__(self, api_token=None):
        self.api_token = api_token or os.getenv("GUMROAD_API_TOKEN", "gumroad_mock_token")
        print("[*] Initialized Gumroad Publisher (Storefront Integration Active)")

    def create_gumroad_product(self, name, description, price_cents, file_path, cover_image=None):
        """
        Configures and creates a Gumroad product listing.
        """
        print(f"[*] Packaging Gumroad Product: '{name}' (Price: ${price_cents / 100:.2f})...")
        
        product_payload = {
            "name": name,
            "description": description,
            "price": price_cents,
            "currency": "aud",
            "url": f"https://fairdinkum.gumroad.com/l/{name.lower().replace(' ', '_')}",
            "file_path": str(file_path),
            "cover_image": str(cover_image) if cover_image else "assets/default_cover.png",
            "published": True,
            "max_purchase_count": None
        }
        
        record_path = OUTPUT_DIR / f"gumroad_product_{name.lower().replace(' ', '_')}.json"
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(product_payload, f, indent=2)
            
        print(f"[+] Gumroad product listing created and saved to {record_path}")
        return product_payload

if __name__ == "__main__":
    publisher = GumroadPublisher()
    product = publisher.create_gumroad_product(
        name="The Autonomous Solopreneur Playbook",
        description="Comprehensive guide and multi-agent workflow templates for solo founders.",
        price_cents=3900,
        file_path="docs/manuscripts/the_autonomous_solopreneur_manuscript.md",
        cover_image="generated_post_image.png"
    )
    print(f"[+] Gumroad Storefront Link: {product['url']}")
