#!/usr/bin/env python3
"""
Sync FormFav Racing Intelligence PDF and bulletins to the Obsidian Racing Vault.
"""
import shutil
from pathlib import Path

DATE = "2026-10-09"
SRC_PDF = Path(f"outputs/formfav/{DATE}/AUS_GALLOPS_FORM_GUIDE_{DATE}.pdf")
VAULT_DIR = Path("/home/brettanthonysjoberg179/Documents/Obsidian Vault/Racing")

def main():
    if not VAULT_DIR.exists():
        print(f"Error: Obsidian Vault Racing directory not found at {VAULT_DIR}")
        return
        
    if SRC_PDF.exists():
        dest_pdf = VAULT_DIR / f"Form Guides {DATE}.pdf"
        shutil.copy2(SRC_PDF, dest_pdf)
        print(f"✅ Copied PDF form guide to Obsidian Vault: {dest_pdf}")
        
    # Also create an Obsidian markdown index note for the date
    note_path = VAULT_DIR / f"Form Guides {DATE} - Index.md"
    note_content = f"""# 🐎 Form Guides & Meeting Index — {DATE}

> Full Australian gallops cards and PDF booklet pulled from FormFav Racing API for race day {DATE}.
> Key meetings: Port Macquarie ($200k Cup), Ballarat ($80k Heat), Launceston, Sunshine Coast, Canberra.

## Linked Documents
- [[Form Guides {DATE}.pdf]]
- [[FormFav API Notes]]
- [[FormFav Trifecta Model]]
"""
    note_path.write_text(note_content)
    print(f"✅ Created Obsidian index note: {note_path}")

if __name__ == "__main__":
    main()
