#!/usr/bin/env python3
"""Upload cover images to all 14 Gumroad products."""
import os
import subprocess
import sys
import json

COVERS_DIR = "/home/brettanthonysjoberg179/gumroad-covers"
GUMROAD = os.path.expanduser("~/.local/bin/gumroad")

# Mapping: product_id -> cover_filename (all 14 products)
PRODUCTS = {
    "04GxzCtpL3JAqYdwx8zatg==": "04GxzCtp_Email-Marketing-Swipe-File-50-Subject-Lines,-20-Se.png",
    "G2ioC8YmZjNOvtKOur7niQ==": "G2ioC8Ym_Digital-Nomad-Starter-Kit-Work-Remotely-From-Anywh.png",
    "UcCPlrS30VtNLXnb4vcXaA==": "UcCPlrS3_Notion-Second-Brain-PARA-Method-Template.png",
    "wQ5hvwF0rP8mxcIiy7eWAw==": "wQ5hvwF0_Freelance-Proposal-Template-That-Wins-Projects.png",
    "Mg9Bcungn-ZICAlY6014yw==": "Mg9Bcung_Digital-Wellness-Planner-30-Day-Anxiety-Reset.png",
    "TjVI8pxWvDygiuPMfP5A-w==": "TjVI8pxW_Content-Creator-Starter-Kit-Scripts,-Captions-&-UG.png",
    "CAV7nDn4E3FjrF_dnqaYgQ==": "CAV7nDn4_ATS-Resume-Template-Pack-5-Clean-Formats-+-Cover-L.png",
    "MBiCUk1vuAgQtVZRXuRIuA==": "MBiCUk1v_Freelance-Notion-Dashboard-Clients,-Invoicing,-Pro.png",
    "R4kxz_YNWWn_DeiqW1y-3w==": "R4kxz_YN_AI-Prompt-Pack-for-Real-Estate-Agents-50-Niche-Spe.png",
    "lnd0IUXYn14ZlBOhFKGaiA==": "lnd0IUXY_GEO-Keyword-Injection-Toolkit-50-Templates-to-Get-.png",
    "JcHK0wf-DRT8tq8pvcTzpA==": "JcHK0wf-_AI-Agent-Starter-Kit.png",
    "FMG2VDvEs2pR_26bXaWgww==": "FMG2VDvE_Digital-Product-Launch-Kit.png",
    "gA2-oxFT7SDjPVX4cR0wyg==": "gA2-oxFT_100-AI-Prompts-for-Content-Creators.png",
    "zsiu1wV_4uqZo9Xue3MU2Q==": "zsiu1wV__100-AI-Prompts-for-Real-Estate-Agents.png",
}

# Products that exist on Gumroad (13 of 14 — zsiu1wV was deleted)
EXISTING_IDS = {
    "04GxzCtpL3JAqYdwx8zatg==": "Email Marketing Swipe File",
    "G2ioC8YmZjNOvtKOur7niQ==": "Digital Nomad Starter Kit",
    "UcCPlrS30VtNLXnb4vcXaA==": "Notion Second Brain",
    "wQ5hvwF0rP8mxcIiy7eWAw==": "Freelance Proposal Template",
    "Mg9Bcungn-ZICAlY6014yw==": "Digital Wellness Planner",
    "TjVI8pxWvDygiuPMfP5A-w==": "Content Creator Starter Kit",
    "CAV7nDn4E3FjrF_dnqaYgQ==": "ATS Resume Template Pack",
    "MBiCUk1vuAgQtVZRXuRIuA==": "Freelance Notion Dashboard",
    "R4kxz_YNWWn_DeiqW1y-3w==": "AI Prompt Pack for Real Estate Agents",
    "lnd0IUXYn14ZlBOhFKGaiA==": "GEO Keyword Injection Toolkit",
    "JcHK0wf-DRT8tq8pvcTzpA==": "AI Agent Starter Kit",
    "FMG2VDvEs2pR_26bXaWgww==": "Digital Product Launch Kit",
    "gA2-oxFT7SDjPVX4cR0wyg==": "100 AI Prompts for Content Creators",
}

def upload_cover(product_id, filename):
    """Upload a single cover image to a Gumroad product."""
    filepath = os.path.join(COVERS_DIR, filename)
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    
    cmd = [GUMROAD, "products", "update", product_id, "--cover-image", filepath]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        return True, result.stdout.strip()[:100]
    else:
        return False, result.stderr.strip()[:200]

def main():
    success = 0
    failed = 0
    skipped = 0
    
    for pid, name in EXISTING_IDS.items():
        filename = PRODUCTS[pid]
        short_name = name[:40]
        print(f"Uploading {short_name}...", end=" ", flush=True)
        
        ok, msg = upload_cover(pid, filename)
        if ok:
            print("✓")
            success += 1
        else:
            print(f"✗ {msg}")
            failed += 1
    
    # Report the missing product
    missing_id = "zsiu1wV_4uqZo9Xue3MU2Q=="
    missing_name = "100 AI Prompts for Real Estate Agents"
    print(f"\nSkipped (not on Gumroad): {missing_name} ({missing_id})")
    skipped += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {success} uploaded, {failed} failed, {skipped} skipped")
    print(f"Total: {success + failed + skipped} products")

if __name__ == "__main__":
    main()
