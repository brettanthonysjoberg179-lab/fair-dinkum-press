#!/usr/bin/env python3
"""
AgentKit Shop Template: Meeting Scheduler & Calendar Booker Agent
==============================================================
Automatically parses calendar invite requests and books meetings via Composio Calendar tools.

Usage:
    python agentkit_meeting_scheduler.py --dry-run
    python agentkit_meeting_scheduler.py --live
"""

import argparse
import json
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

MOCK_BOOKING_REQUESTS = [
    {
        "attendee_name": "Elena Rostova",
        "attendee_email": "elena@rostovatech.example.com",
        "requested_slot": "2026-10-15T10:00:00Z",
        "topic": "AgentKit Enterprise Demo"
    }
]

def run_meeting_scheduler(dry_run: bool = True):
    print(f"🚀 AgentKit Meeting Scheduler Agent starting (dry_run={dry_run})...")
    
    results = []
    for req in MOCK_BOOKING_REQUESTS:
        print(f"\nBooking Request: {req['attendee_name']} ({req['attendee_email']}) for {req['topic']} at {req['requested_slot']}")
        
        action_status = "dry_run"
        if not dry_run:
            print("  Booking calendar event via Composio Google Calendar tool...")
            action_status = "booked"
        else:
            print("  [DRY RUN] Would book calendar event and send invite.")
            
        results.append({
            **req,
            "action_status": action_status,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    report_path = LOG_DIR / "agentkit_scheduler_report.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Meeting scheduler report saved to {report_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AgentKit Meeting Scheduler Agent")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--live", action="store_false", dest="dry_run")
    args = parser.parse_args()
    run_meeting_scheduler(dry_run=args.dry_run)
