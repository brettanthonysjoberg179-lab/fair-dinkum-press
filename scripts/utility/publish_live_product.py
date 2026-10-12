import os
import json
import asyncio
import sys
from pathlib import Path

# Set environment for live publish BEFORE importing config/app
os.environ["DRY_RUN"] = "false"

sys.path.insert(0, ".")
import digital_product_workforce.config as dp_config
from digital_product_workforce.config import Settings
dp_config.settings = Settings(dry_run=False)

import digital_product_workforce.app as dp_app
dp_app.settings = dp_config.settings

async def main():
    args = {
        "title": "The 1-Person AI Enterprise: How to Build, Automate, and Scale a $50k/Month Micro-Business Using Model Context Protocol (MCP) & Cloudflare Agents",
        "description": "The complete operational playbook and codebase for building a $50k/month micro-business powered by autonomous AI agent swarms, Model Context Protocol (MCP), and Cloudflare edge infrastructure.",
        "price": 49.00,
        "asset_path": "digital_product_workforce/outputs/prod-one-person-ai-enterprise-001/package/01-gumroad-package.zip"
    }
    
    result = await dp_app._tool_publish_storefront_item(args)
    print("Live Publish Result:", json.dumps(result, indent=2))
    
    listing_id = result.get("listing_id")
    listing_url = result.get("listing_url")
    
    product_dir = Path("digital_product_workforce/outputs/prod-one-person-ai-enterprise-001")
    
    # Update 00-product-brief.json
    brief_path = product_dir / "00-product-brief.json"
    if brief_path.exists():
        brief = json.loads(brief_path.read_text())
        brief["status"] = f"published (LIVE - listing {listing_id})"
        brief["live_listing_id"] = listing_id
        brief["live_listing_url"] = listing_url
        brief_path.write_text(json.dumps(brief, indent=2))
        
    # Write publish/03-publish-log.json
    publish_log_path = product_dir / "publish" / "03-publish-log.json"
    publish_log_path.parent.mkdir(parents=True, exist_ok=True)
    publish_log_path.write_text(json.dumps({
        "status": "success",
        "listing_id": listing_id,
        "listing_url": listing_url,
        "price": 49.00,
        "published_live": True
    }, indent=2))
    
    print(f"Successfully published live as {listing_id} at {listing_url}")

asyncio.run(main())
