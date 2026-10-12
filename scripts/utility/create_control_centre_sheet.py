#!/usr/bin/env python3
"""
Create Google Sheets Control Centre for MCP Server Agents and Business Metrics.
"""

import os
import sys
from pathlib import Path

# Data structures for the Control Centre
MCP_AGENTS = [
    ["Agent Name", "Module / Path", "Interface", "Status", "Last Health Check", "Description"],
    ["MCP Server Workforce", "mcp-server-workforce/", "MCP Server", "Active", "2026-10-04", "Multi-agent orchestration & tool execution server"],
    ["Composio Telegram MCP", "composio-telegram-mcp/", "MCP / Telegram", "Active", "2026-10-04", "Telegram bridge & tool router"],
    ["Ollama Gemma MCP", "ollama-gemma-mcp/", "MCP / LLM", "Active", "2026-10-04", "Local Gemma model inference & finetuning MCP"],
    ["Inventory Manager Agent", "inventory-manager-agent/", "CLI / MCP", "Active", "2026-10-04", "Product inventory & Stripe/Gumroad sync"],
    ["Lawyer Review Agent", "lawyer-review-agent/", "MCP / Audit", "Active", "2026-10-04", "Compliance & legal audit agent"],
    ["My G Drive Agent", "my-g-drive-agent/", "Agent / Drive", "Active", "2026-10-04", "Google Drive backup, dedupe & sync agent"],
    ["Email Trigger Agent", "email_trigger_agent.py", "Automation", "Active", "2026-10-04", "Autonomous email sequence & inquiry responder"],
    ["FormFav Gallops Agent", "fair-dinkum-publishing-agent-workflowz/", "API / Racing", "Active", "2026-10-04", "Horse racing form guide & trifecta predictor"]
]

BUSINESS_METRICS = [
    ["Metric Name", "Category", "Target", "Current Value", "Status", "Notes"],
    ["Micro-Product Sales ($49-$97)", "Revenue", "$5,000 / mo", "$2,450", "On Track", "FOUND ON AI & Agent Workflows"],
    ["Mid-Ticket Playbooks ($149)", "Revenue", "$10,000 / mo", "$4,800", "Growing", "AU AI Compliance Playbook (Privacy Act 1988)"],
    ["High-Ticket Consulting ($1,500)", "Revenue", "$15,000 / mo", "$4,500", "Active", "DFY AI Compliance Audits & Reports"],
    ["Programmatic SEO Articles", "Traffic", "50 articles", "15 live", "Expanding", "Targeting regional AU B2B niches"],
    ["Email Sequences & Triggers", "Automation", "100% automated", "Active", "Operational", "Composio Gmail & webhook triggers"],
    ["Obsidian Racing Vault", "Intelligence", "Daily fetch", "Active (71 races)", "Operational", "FormFav gallops & trifecta database sync"]
]

PRODUCT_INVENTORY = [
    ["Product Name", "Tier", "Price", "Platform", "Status", "Source File / Path"],
    ["FOUND ON AI", "Micro-Product", "$97", "Gumroad / Stripe", "Active", "100-AI-Prompts-for-Content-Creators.pdf"],
    ["5 Niche AI Agent Workflows", "Micro-Product", "$97", "Gumroad / Stripe", "Active", "ai-agent-starter-kit.pdf"],
    ["Geo-Toolkit Templates", "Micro-Product", "$49", "Gumroad / Stripe", "Active", "geo-toolkit/"],
    ["AU AI Compliance Playbook", "Mid-Ticket", "$149", "Book Hub / Stripe", "Active", "AI_COMPLIANCE_LAUNCH_PACKET.md"],
    ["Empire Super-Bundle", "High-Ticket", "$297", "Storefront", "Active", "Complete asset inventory bundle"],
    ["DFY AI Compliance Audit", "Service", "$1,500", "Calendly / Direct", "Active", "Consulting & Report"]
]

def generate_csv_outputs():
    output_dir = Path("outputs/control_centre")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    import csv
    
    for name, data in [("MCP_Agents", MCP_AGENTS), ("Business_Metrics", BUSINESS_METRICS), ("Product_Inventory", PRODUCT_INVENTORY)]:
        file_path = output_dir / f"{name}.csv"
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print(f"Generated CSV: {file_path}")

if __name__ == "__main__":
    generate_csv_outputs()
    print("\nControl Centre CSV files successfully generated in outputs/control_centre/")
    print("These can be uploaded directly to Google Sheets or managed via Composio / Google Drive API.")
