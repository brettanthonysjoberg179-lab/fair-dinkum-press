#!/usr/bin/env python3
"""Batch update agents to add formula tool support."""
import re
import sys
from pathlib import Path

AGENT_DIRS = [
    "agents/analytics/agent.py",
    "agents/article_writer/agent.py",
    "agents/audience_intelligence/agent.py",
    "agents/content_strategy/agent.py",
    "agents/creation/copywriting_agent.py",
    "agents/creation/cover_designer_agent.py",
    "agents/creation/digital_product_creator_agent.py",
    "agents/creation/pageonator_agent.py",
    "agents/creation/writer_agent.py",
    "agents/discovery/digital_product_concept_agent.py",
    "agents/discovery/ebook_research_agent.py",
    "agents/discovery/research_agent.py",
    "agents/discovery/seo_research_agent.py",
    "agents/discovery/trend_agent.py",
    "agents/distribution/fulfillment_agent.py",
    "agents/distribution/products_packager_agent.py",
    "agents/distribution/publisher_agent.py",
    "agents/distribution/sales_agent.py",
    "agents/ebo/agent.py",
    "agents/facebook_intelligence/agent.py",
    "agents/fact_check/agent.py",
    "agents/gumroad_intelligence/agent.py",
    "agents/linkedin_intelligence/agent.py",
    "agents/management/business_automation_agent.py",
    "agents/management/business_manager_agent.py",
    "agents/management/business_planner_agent.py",
    "agents/management/financial_adviser_agent.py",
    "agents/management/workflow_planner_agent.py",
    "agents/optimisation/agent.py",
    "agents/orchestrator/agent.py",
    "agents/payhip_intelligence/agent.py",
    "agents/publishing/agent.py",
    "agents/qa/agent.py",
    "agents/reddit_intelligence/agent.py",
    "agents/repurposing/agent.py",
    "agents/seo/agent.py",
    "agents/social_content/agent.py",
    "agents/tiktok_intelligence/agent.py",
    "agents/trend_intelligence/agent.py",
    "agents/video_script/agent.py",
    "agents/wix_intelligence/agent.py",
    "agents/wordpress_intelligence/agent.py",
    "agents/x_intelligence/agent.py",
]

PROJECT_ROOT = Path(__file__).parent

def update_agent(filepath):
    content = filepath.read_text()
    original = content
    
    # 1. Add "formula" to allowed_tools if it's a class attribute list
    if 'allowed_tools = [' in content and '"formula"' not in content:
        # Match the pattern with "formula" added at end
        content = re.sub(
            r'allowed_tools = \[([^\]]+)\]',
            lambda m: f'allowed_tools = [{m.group(1).rstrip(",")}, "formula"]',
            content
        )
    
    # 2. Add load_skill("formula") after load_skill("composio_tooling") or last load_skill in __init__
    if 'load_skill("composio_tooling")' in content and 'load_skill("formula")' not in content:
        content = re.sub(
            r'(self\.load_skill\("composio_tooling"\))',
            r'\1\n        self.load_skill("formula")',
            content
        )
    
    if content != original:
        filepath.write_text(content)
        print(f"Updated: {filepath.relative_to(PROJECT_ROOT)}")
        return True
    return False

def main():
    updated = 0
    for agent_path in AGENT_DIRS:
        filepath = PROJECT_ROOT / agent_path
        if not filepath.exists():
            print(f"SKIP: {filepath} (not found)")
            continue
        if update_agent(filepath):
            updated += 1
    
    print(f"\nUpdated {updated} agents")

if __name__ == "__main__":
    main()