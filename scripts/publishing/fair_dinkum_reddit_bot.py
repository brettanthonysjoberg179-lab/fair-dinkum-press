#!/usr/bin/env python3
"""
Fair Dinkum Reddit Publishing & Marketing Bot
Automates posting high-value technical/architectural breakdowns and product teasers
to targeted subreddits via Composio's Reddit integration.
"""

import os
import sys
import json
import subprocess
from datetime import datetime

DEFAULT_SUBREDDITS = [
    "Entrepreneur",
    "SaaS",
    "IndieHackers",
    "AI_Agents",
    "ChatGPT"
]

CAMPAIGNS = {
    "solopreneur_enterprise": {
        "subreddit": "Entrepreneur",
        "title": "How I stopped being a manual 'prompt jockey' and built a 24/7 multi-agent publishing enterprise (Complete Architecture Breakdown)",
        "text": """For the past two years, I fell into what I call the Chatbot Trap. I was opening browser tabs, typing ad-hoc prompts, and manually stitching together outputs. Even with state-of-the-art models, my human attention remained the ultimate operational bottleneck.

Last month, I decided to fix this. I shifted my role from a manual doer to the Chief Architect of an autonomous multi-agent AI workforce. 

Today, I’m open-sourcing and publishing the complete operational blueprint behind this transition in my new masterclass: "The Autonomous Solopreneur: Building & Scaling Multi-Agent AI Enterprises."

Here is the exact architecture we built and deployed:

1. Role-Specialized Agent Swarms:
- The Researcher: Gathers market data and long-tail keyword matrices.
- The Writer/Editor: Synthesizes structured markdown manuscripts with strict stylistic constraints.
- The Compliance Auditor: Scans every asset against regulatory checklists and negative constraints.
- The Publisher: Packages assets and interfaces with headless storefront APIs.

2. Tiered Memory & Vector RAG:
- Global Memory (GEMINI.md) for cross-project preferences.
- Team-Shared Instructions committed to version control.
- Private Project Memory (MEMORY.md) for local operational state.
- Vector DB Retrieval for institutional recall across past research.

3. Automated Pipelines & Headless Monetization:
- Programmatic SEO (pSEO): Generating structured content matrices at scale.
- Self-Healing QA Loops: Catching formatting errors automatically before human review.
- Headless Storefronts: Packaging validated EPUBs and cover art into ZIP bundles and syncing inventory to Airtable and Gumroad.

We’ve packaged the 10-chapter EPUB, cover art, automated email drip sequences, and companion workbook into a complete digital product kit (Live on Gumroad & synced to Airtable via Fair Dinkum Publishing Agent Workflowz).

Are you still using chat interfaces for business operations, or have you started orchestrating autonomous agent swarms? Happy to answer any questions about the technical architecture below!""",
        "flair_id": "c2f22a12-e1d8-11e3-a77b-12313b0a74a7"
    },
    "ai_toolkit": {
        "subreddit": "SaaS",
        "title": "We open-sourced 50 production-ready AI prompts and automation workflows that generate revenue 24/7",
        "text": """Most AI prompts fail in production because they lack system constraints, error-handling guardrails, and structured output schemas. 

Over the last 6 months building digital product workflows, we curated and battle-tested 50 high-impact AI prompts specifically engineered for content creators, solo founders, and SaaS developers.

Included in the toolkit:
- Programmatic SEO & Content Generation pipelines
- Automated Gumroad & Stripe product packagers
- Compliance & Legal Audit generators
- Multi-agent workflow orchestrators

We packaged everything into the Fair Dinkum AI Toolkit (.90 AUD on Gumroad). 

What prompt frameworks do you rely on for production AI apps? Let's discuss below!""",
        "flair_id": ""
    }
}

def publish_post(campaign_key):
    if campaign_key not in CAMPAIGNS:
        print(f"Error: Campaign '{campaign_key}' not found.")
        print(f"Available campaigns: {list(CAMPAIGNS.keys())}")
        return False

    campaign = CAMPAIGNS[campaign_key]
    subreddit = campaign["subreddit"]
    title = campaign["title"]
    text = campaign["text"]
    flair_id = campaign.get("flair_id", "")

    payload = {
        "subreddit": subreddit,
        "title": title,
        "text": text,
        "kind": "self"
    }
    if flair_id:
        payload["flair_id"] = flair_id

    print(f"[{datetime.now().isoformat()}] Publishing campaign '{campaign_key}' to r/{subreddit}...")
    cmd = ["composio", "execute", "REDDIT_CREATE_REDDIT_POST", "-d", json.dumps(payload)]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)

    # Log execution
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "campaign": campaign_key,
        "subreddit": subreddit,
        "title": title,
        "stdout": res.stdout,
        "stderr": res.stderr,
        "returncode": res.returncode
    }
    
    log_file = "reddit_publish_history.json"
    history = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r") as f:
                history = json.load(f)
        except Exception:
            pass
    history.append(log_entry)
    with open(log_file, "w") as f:
        json.dump(history, f, indent=2)

    return res.returncode == 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fair Dinkum Reddit Publishing Bot")
    parser.add_argument("--campaign", choices=list(CAMPAIGNS.keys()), default="solopreneur_enterprise", help="Campaign key to execute")
    parser.add_argument("--list", action="store_true", help="List available campaigns")
    args = parser.parse_args()

    if args.list:
        print("Available Campaigns:")
        for k, v in CAMPAIGNS.items():
            print(f"  - {k}: r/{v['subreddit']} -> {v['title'][:60]}...")
        sys.exit(0)

    success = publish_post(args.campaign)
    if success:
        print("Successfully executed Reddit publishing campaign!")
    else:
        print("Publishing encountered errors or warnings.")
