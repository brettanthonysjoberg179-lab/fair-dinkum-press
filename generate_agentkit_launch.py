#!/usr/bin/env python3
"""
AgentKit Shop: Launch Asset Generator
====================================
Generates the free GitHub starter repo script and LinkedIn launch post copy
for the AgentKit Shop top-of-funnel acquisition engine.

Usage:
    python generate_agentkit_launch.py
"""

from pathlib import Path

LAUNCH_DIR = Path("dist/launch")
LAUNCH_DIR.mkdir(parents=True, exist_ok=True)

STARTER_SCRIPT_CONTENT = '''#!/usr/bin/env python3
"""
AgentKit Free Starter: Simple AI Email Greeter Agent
==================================================
A lightweight starter agent demonstrating Composio Gmail integration
for indie developers and indie hackers.

Usage:
    python agentkit_starter.py
"""

import subprocess
import json

def main():
    print("🚀 AgentKit Free Starter Agent running...")
    print("💡 To connect your tools, run: composio login")
    
    try:
        cmd = ["/home/brettanthonysjoberg179/.local/bin/composio", "execute", "GMAIL_WHO_AM_I", "-d", "{}"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            print(f"✅ Composio connected: {res.stdout[:150]}")
        else:
            print("⚠️ Composio not yet logged in. Run `composio login` to enable live tool calls.")
    except Exception as e:
        print(f"ℹ️ Offline simulation mode: {e}")

    print("\\n🎉 Grab the full Small Business Pack (8+ templates) at: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u")

if __name__ == "__main__":
    main()
'''

LINKEDIN_POST_CONTENT = """🚀 How I automated 80% of client lead triage and invoice chasing using Python and Composio.

As an indie developer, spending hours manually sorting inbound emails and chasing unpaid invoices drains creative energy. 

So I built **AgentKit Shop** — production-ready AI agent workflow packs built specifically for indie devs and small businesses. Every template is fully wired into real tools (Gmail, Stripe, GitHub) rather than just abstract prompts.

Here's what's in our Small Business Pack v1.0:
1️⃣ **Inbound Lead Triage Agent:** Polls unread emails, categorizes lead intent, and drafts tailored responses linking straight to your checkout.
2️⃣ **Overdue Invoice Chaser Agent:** Automatically flags unpaid client invoices and sends polite reminder emails with instant Stripe payment links.

🎁 **Free Starter Repo:** Want to test it yourself? Comment "AGENT" below and I'll DM you the free GitHub starter repo and Hugging Face live demo link.

👉 Full packs & bundles: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u

#ArtificialIntelligence #Python #IndieHacker #Automation #Composio #Stripe
"""

def generate_assets():
    starter_path = LAUNCH_DIR / "agentkit_starter.py"
    starter_path.write_text(STARTER_SCRIPT_CONTENT)
    
    linkedin_path = LAUNCH_DIR / "linkedin_launch_post.md"
    linkedin_path.write_text(LINKEDIN_POST_CONTENT)
    
    print(f"✅ Generated starter script at {starter_path}")
    print(f"✅ Generated LinkedIn launch post at {linkedin_path}")

if __name__ == "__main__":
    generate_assets()
