#!/usr/bin/env python3
"""
Generate complete Australian race cards & trifecta predictions for 2026-10-08 (Orange & York).
"""
import subprocess
import json
from pathlib import Path

DATE = "2026-10-08"
TRACKS = ["orange", "york"]
OUTPUT_FILE = Path(f"outputs/formfav/{DATE}/AUS_RACES_PREDICTIONS_{DATE}.md")

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
    report.append(f"# 🦘 Australian Racing Intelligence & Trifecta Predictions — {DATE}\n")
    report.append("Generated via FormFav API & Algorithmic Trifecta Engine.\n")
    
    for m in meetings_data.get("meetings", []):
        slug = m.get("slug")
        country = m.get("country")
        if country == "au" and slug in TRACKS:
            track_name = m.get("track", slug.title())
            report.append(f"\n## 🏟️ Meeting: {track_name} (Australia)\n")
            
            for r in m.get("races", []):
                rnum = r.get("raceNumber")
                rname = r.get("raceName", f"Race {rnum}")
                dist = r.get("distance", "N/A")
                cond = r.get("condition", "N/A")
                class_str = r.get("raceClass", "N/A")
                abandoned = r.get("abandoned", False)
                
                report.append(f"### Race {rnum}: {rname} ({dist} | Condition: {cond} | Class: {class_str})")
                
                if abandoned:
                    report.append("- ⚠️ *Race Status: ABANDONED*\n")
                    continue
                
                card = run_formfav(["race-card", DATE, slug, str(rnum)])
                runners = card.get("runners", [])
                
                if runners:
                    # Filter out scratched runners
                    active_runners = [x for x in runners if not x.get("scratched", False)]
                    
                    # Sort by barrier and weight heuristic
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
                        
                        report.append(f"- 🥇 **1st (Win):** {sel1} (Barrier {sorted_runners[0].get('barrier', '-')}, Wt {sorted_runners[0].get('weight', '-')})")
                        report.append(f"- 🥈 **2nd (Place):** {sel2} (Barrier {sorted_runners[1].get('barrier', '-')}, Wt {sorted_runners[1].get('weight', '-')})")
                        report.append(f"- 🥉 **3rd (Show):** {sel3} (Barrier {sorted_runners[2].get('barrier', '-')}, Wt {sorted_runners[2].get('weight', '-')})")
                        report.append(f"- 💎 *Trifecta Tip:* Box {sel1} / {sel2} / {sel3}\n")
                        
                        report.append("**Full Runner Field:**")
                        for run in active_runners:
                            report.append(f"  - #{run.get('number')} **{run.get('name')}** (Jockey: {run.get('jockey', 'N/A')}, Trainer: {run.get('trainer', 'N/A')}, Barrier: {run.get('barrier', '-')}, Wt: {run.get('weight', '-')})")
                        report.append("")
                    else:
                        report.append("- *Field:* All runners scratched.\n")
                else:
                    report.append("- *Predictions:* Field analysis pending.\n")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(report))
    print(f"✅ Australian races report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
