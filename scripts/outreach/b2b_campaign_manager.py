#!/usr/bin/env python3
"""
Dual-Track B2B Outreach Campaign Manager
========================================
Manages targeted outreach campaigns for:
1. Track A (Founders): Pitching AgentKit Small Business Automation Pack ($19).
2. Track B (Enterprise Executives): Offering Custom AI Compliance Audits & Playbook ($1,500).

Tracks dispatch status, personalization, and follow-ups in SQLite.
"""

import os
import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = "data/outreach_campaigns.db"

def init_outreach_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prospects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            title TEXT,
            track TEXT CHECK(track IN ('founder', 'enterprise')),
            status TEXT DEFAULT 'pending',
            last_contacted TIMESTAMP
        )
    """)
    conn.commit()
    return conn

TRACK_MESSAGES = {
    "founder": {
        "subject": "Automating {company}'s lead triage & invoicing with Python",
        "body": "Hi {name},\n\nNoticed {company} is scaling fast. Most founders I talk to lose 10-15 hours a week on manual lead triage, overdue invoice chasing, and CRM data entry.\n\nWe built AgentKit—a production-ready 5-workflow Python automation pack designed specifically to eliminate these bottlenecks in under an hour.\n\nTake a look here: https://buy.stripe.com/8x26oJ4Z30rx0zb6rKbMQ0u\n\nBest,\nBrett"
    },
    "enterprise": {
        "subject": "AI Privacy Act & Automated Decision Compliance at {company}",
        "body": "Hi {name},\n\nAs {company} expands its use of AI models and automated decision-making, navigating the Privacy Act 1988 (Cth) and OAIC guidelines is critical to avoid hidden regulatory exposure.\n\nAt Fair Dinkum Press, we help enterprise leaders audit their AI stacks and implement robust Human-in-the-Loop (HITL) guardrails.\n\nWould you be open to a brief discussion or reviewing our enterprise AI Compliance Playbook?\n\nBest regards,\nBrett"
    }
}

def seed_sample_prospects(conn: sqlite3.Connection):
    sample_prospects = [
        ("Sarah Jenkins", "sarah@techstartup.io", "TechStartup", "CEO", "founder"),
        ("Michael Chang", "m.chang@enterprisebank.com.au", "Enterprise Bank", "Chief Risk Officer", "enterprise"),
        ("David Miller", "david@growthagency.co", "Growth Agency", "Founder", "founder"),
        ("Rachel Vance", "rachel@healthcorp.com.au", "HealthCorp", "General Counsel", "enterprise")
    ]
    for name, email, company, title, track in sample_prospects:
        conn.execute(
            "INSERT OR IGNORE INTO prospects (name, email, company, title, track) VALUES (?, ?, ?, ?, ?)",
            (name, email, company, title, track)
        )
    conn.commit()

def run_campaign(dry_run: bool = True):
    conn = init_outreach_db()
    seed_sample_prospects(conn)
    
    cursor = conn.execute("SELECT * FROM prospects WHERE status = 'pending'")
    prospects = cursor.fetchall()
    
    logger.info(f"🚀 Starting B2B Outreach Campaign (Dry Run: {dry_run}). Found {len(prospects)} pending prospects.")
    
    dispatched_count = 0
    for p in prospects:
        track = p["track"]
        template = TRACK_MESSAGES[track]
        
        subject = template["subject"].format(name=p["name"], company=p["company"])
        body = template["body"].format(name=p["name"], company=p["company"])
        
        logger.info(f"\n--- [TRACK: {track.upper()}] To: {p['name']} <{p['email']}> ({p['company']} - {p['title']}) ---")
        logger.info(f"Subject: {subject}\n\n{body}\n")
        
        if not dry_run:
            conn.execute("UPDATE prospects SET status = 'sent', last_contacted = CURRENT_TIMESTAMP WHERE id = ?", (p["id"],))
            conn.commit()
        dispatched_count += 1
        
    conn.close()
    logger.info(f"✅ Successfully processed {dispatched_count} outreach messages.")

if __name__ == "__main__":
    run_campaign(dry_run=True)
