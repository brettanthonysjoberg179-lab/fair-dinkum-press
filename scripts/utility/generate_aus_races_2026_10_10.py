#!/usr/bin/env python3
"""
Generate complete Australian race cards, form guides, and trifecta predictions for 2026-10-10.
Tracks: Albury, Alice Springs, Ascot, Port Macquarie, Rosehill, Warwick.
"""
import subprocess
import json
from pathlib import Path
import shutil
import os

# Load FORMFAV_API_KEY from ~/.env
env_file = Path.home() / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line.startswith("FORMFAV_API_KEY="):
            os.environ["FORMFAV_API_KEY"] = line.split("=", 1)[1].strip("'\" ")

DATE = "2026-10-10"
TRACKS = ["albury", "alice-springs", "ascot", "port-macquarie", "rosehill", "warwick"]
OUT_DIR = Path(f"outputs/formfav/{DATE}")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_MD = OUT_DIR / f"AUS_GALLOPS_FORM_GUIDE_{DATE}.md"
ROOT_MD = Path(f"AUS_GALLOPS_FORM_GUIDE_{DATE}.md")

def run_formfav(cmd_args):
    cmd = ["python3", "formfav.py"] + cmd_args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        try:
            return json.loads(res.stdout)
        except Exception:
            return {"raw": res.stdout}
    return {}

def main():
    print(f"Fetching Australian meetings for {DATE}...")
    meetings_data = run_formfav(["meetings", DATE])
    
    report = []
    report.append(f"# 🦘 Australian Racing Intelligence & Form Guide — {DATE}\n")
    report.append("> Pulled via FormFav Racing API engine. Includes meeting cards, runners, jockeys, trainers, barriers, weights, conditions, prize money, and algorithmic trifecta tips.\n")
    report.append("---")
    
    meetings_found = 0
    for m in meetings_data.get("meetings", []):
        slug = m.get("slug")
        country = m.get("country")
        if country == "au" and slug in TRACKS:
            meetings_found += 1
            track_name = m.get("track", slug.title())
            report.append(f"\n## 🏟️ Meeting: {track_name} (Australia / {slug})\n")
            
            for r in m.get("races", []):
                rnum = r.get("raceNumber")
                rname = r.get("raceName", f"Race {rnum}")
                dist = r.get("distance", "N/A")
                cond = r.get("condition", "N/A")
                weather = r.get("weather", "N/A")
                class_str = r.get("raceClass", "N/A")
                prize = r.get("prizeMoney", "N/A")
                abandoned = r.get("abandoned", False)
                
                prize_fmt = f"${int(prize):,}" if str(prize).isdigit() else prize
                report.append(f"### Race {rnum}: {rname}")
                report.append(f"- **Distance:** {dist} | **Class:** {class_str} | **Track Condition:** {cond} | **Weather:** {weather} | **Prize:** {prize_fmt}")
                
                if abandoned:
                    report.append("- ⚠️ *Race Status: ABANDONED*\n")
                    continue
                
                card = run_formfav(["race-card", DATE, slug, str(rnum)])
                runners = card.get("runners", [])
                
                if runners:
                    active_runners = [x for x in runners if not x.get("scratched", False)]
                    
                    # Sort by barrier and weight heuristic for trifecta selection
                    sorted_runners = sorted(
                        active_runners,
                        key=lambda x: (
                            int(x.get("barrier", 99)) if str(x.get("barrier", "")).isdigit() else 99,
                            float(x.get("weight", 56.0)) if str(x.get("weight", "")).replace(".","").isdigit() else 56.0
                        )
                    )
                    
                    if sorted_runners:
                        sel1 = sorted_runners[0].get("name", "Runner A")
                        sel2 = sorted_runners[1].get("name", "Runner B") if len(sorted_runners) > 1 else "Runner B"
                        sel3 = sorted_runners[2].get("name", "Runner C") if len(sorted_runners) > 2 else "Runner C"
                        
                        report.append(f"\n**🎯 Trifecta Selection Tips:**")
                        report.append(f"- 🥇 **1st (Win):** {sel1} (Barrier {sorted_runners[0].get('barrier', '-')}, Wt {sorted_runners[0].get('weight', '-')})")
                        report.append(f"- 🥈 **2nd (Place):** {sel2} (Barrier {sorted_runners[1].get('barrier', '-')}, Wt {sorted_runners[1].get('weight', '-')})")
                        report.append(f"- 🥉 **3rd (Show):** {sel3} (Barrier {sorted_runners[2].get('barrier', '-')}, Wt {sorted_runners[2].get('weight', '-')})")
                        report.append(f"- 💎 *Box Trifecta:* {sel1} / {sel2} / {sel3}\n")
                    
                    report.append("**Full Field Runners:**")
                    for run in active_runners:
                        r_num = run.get("number", "-")
                        r_name = run.get("name", "Unknown")
                        jockey = run.get("jockey", "N/A")
                        trainer = run.get("trainer", "N/A")
                        barrier = run.get("barrier", "-")
                        weight = run.get("weight", "-")
                        rating = run.get("rating", "-")
                        report.append(f"  - #{r_num} **{r_name}** | Jockey: {jockey} | Trainer: {trainer} | Barrier: {barrier} | Weight: {weight}kg | Rating: {rating}")
                    report.append("")
                else:
                    report.append("- *Field Details:* Pending runner publication.\n")

    full_text = "\n".join(report)
    OUTPUT_MD.write_text(full_text)
    ROOT_MD.write_text(full_text)
    print(f"✅ Form guide report generated successfully for {meetings_found} Australian meetings.")
    print(f"   Saved to {OUTPUT_MD} and {ROOT_MD}")

    # Sync to Obsidian vault
    vault_dir = Path("/home/brettanthonysjoberg179/Documents/Obsidian Vault/Racing")
    if vault_dir.exists():
        obsidian_note = vault_dir / f"Form Guides {DATE}.md"
        obsidian_note.write_text(full_text)
        print(f"✅ Synced form guide to Obsidian Vault: {obsidian_note}")

if __name__ == "__main__":
    main()
