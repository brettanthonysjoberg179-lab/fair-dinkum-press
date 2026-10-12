#!/usr/bin/env python3
"""
AgentKit Shop: Vertical Pack Packager (All 5 Templates - $19 Bundle)
===================================================================
Packages all 5 AgentKit templates, documentation, and configuration files into a clean
distribution ZIP archive ready for Gumroad delivery ($19 bundle) and GitHub repository sync.

Usage:
    python package_agentkit_pack.py
"""

import zipfile
from pathlib import Path

PACK_NAME = "AgentKit-SmallBusiness-Pack-Complete-v1.0"
DIST_DIR = Path("dist")
DIST_DIR.mkdir(exist_ok=True)

FILES_TO_PACK = [
    "agentkit_lead_triage.py",
    "agentkit_invoice_chaser.py",
    "agentkit_lead_enrichment.py",
    "agentkit_followup_sequencer.py",
    "agentkit_meeting_scheduler.py",
]

def create_readme() -> Path:
    readme_path = Path("AGENTKIT_README.md")
    readme_path.write_text("""# AgentKit Shop: Small Business Automation Pack ($19 Full Edition)

Production-ready AI agent workflow packs powered by Python, Composio, and Stripe.

## Included Templates (5 Workflows)
1. **Inbound Lead Triage & Gmail Reply Draft Agent** (`agentkit_lead_triage.py`)
   - Automatically polls unread emails, classifies lead intent, and drafts tailored responses linking to your Stripe checkout.
2. **Overdue Invoice Chaser Agent** (`agentkit_invoice_chaser.py`)
   - Flags unpaid invoices and sends polite automated reminder emails with instant Stripe payment links.
3. **Lead Enrichment & CRM Sync Agent** (`agentkit_lead_enrichment.py`)
   - Enriches inbound leads with company data and syncs them to your CRM/Google Sheets via Composio tools.
4. **Automated Follow-up Sequencer Agent** (`agentkit_followup_sequencer.py`)
   - Schedules multi-step email follow-up sequences for unresponsive prospects via Composio Gmail tools.
5. **Meeting Scheduler & Calendar Booker Agent** (`agentkit_meeting_scheduler.py`)
   - Automatically parses calendar invite requests and books meetings via Composio Calendar tools.

## Quick Start
1. Install dependencies:
   ```bash
   pip install composio-core requests
   ```
2. Authenticate Composio:
   ```bash
   composio login
   ```
3. Run templates in dry-run mode:
   ```bash
   python agentkit_lead_triage.py --dry-run
   python agentkit_invoice_chaser.py --dry-run
   python agentkit_lead_enrichment.py --dry-run
   python agentkit_followup_sequencer.py --dry-run
   python agentkit_meeting_scheduler.py --dry-run
   ```

## Support & Updates
- Get more packs: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u
- GitHub Repo: Private access included with purchase.
""")
    return readme_path

def package_pack():
    print(f"📦 Packaging {PACK_NAME} ($19 Complete Edition)...")
    readme = create_readme()
    
    zip_path = DIST_DIR / f"{PACK_NAME}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(readme, arcname="README.md")
        for f in FILES_TO_PACK:
            p = Path(f)
            if p.exists():
                zf.write(p, arcname=p.name)
                print(f"  Added: {p.name}")
            else:
                print(f"  Warning: {f} not found.")
                
    print(f"✅ Successfully created package: {zip_path} ({zip_path.stat().st_size} bytes)")

if __name__ == "__main__":
    package_pack()
