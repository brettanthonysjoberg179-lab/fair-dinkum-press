#!/usr/bin/env python3
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

    print("\n🎉 Grab the full Small Business Pack (8+ templates) at: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u")

if __name__ == "__main__":
    main()
