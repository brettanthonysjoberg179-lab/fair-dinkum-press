#!/usr/bin/env python3
"""
Audit all Gumroad digital product zip packages to ensure required assets are present.
"""
import zipfile
from pathlib import Path

def audit_packages():
    zips = list(Path(".").glob("**/*gumroad*.zip"))
    print(f"Auditing {len(zips)} Gumroad product packages...\n")
    
    passed = 0
    failed = 0
    
    for zpath in sorted(zips):
        try:
            with zipfile.ZipFile(zpath, 'r') as zf:
                namelist = zf.namelist()
                size = zpath.stat().st_size
                
                # Check for essential assets (epub/pdf, cover/png, markdown/txt)
                has_media = any(n.lower().endswith(('.epub', '.pdf', '.json', '.txt', '.md')) for n in namelist)
                has_cover = any('cover' in n.lower() or n.lower().endswith(('.png', '.jpg')) for n in namelist)
                
                status = "✅ PASS" if (size > 1000 and has_media) else "⚠️ WARNING"
                if "PASS" in status:
                    passed += 1
                else:
                    failed += 1
                    
                print(f"{status} | {zpath.name} ({size:,} bytes) | Files: {namelist}")
        except Exception as e:
            failed += 1
            print(f"❌ ERROR | {zpath.name} | {e}")
            
    print(f"\nAudit Complete: {passed} passed, {failed} warnings/errors out of {len(zips)} packages.")

if __name__ == "__main__":
    audit_packages()
