import os
import logging
from datetime import datetime
from scripts.autonomous.database import get_db_connection, log_agent_action, save_lead

logger = logging.getLogger(__name__)

class LeadTriageEngine:
    """
    Client Lead Triage & Sales Outreach Engine for Autonomous Enterprise Agents.
    Scores inbound leads based on ICP criteria, drafts personalized sales outreach,
    and synchronizes records to the CRM database.
    """
    def __init__(self, dry_run=True, db_path=None):
        self.dry_run = dry_run
        self.db_path = db_path

    def score_and_triage(self, lead: dict) -> dict:
        """
        Scores an inbound lead (0-100) and categorizes into intent tiers.
        Criteria:
        - Email domain (corporate vs free gmail/yahoo/edu)
        - Executive/decision-maker title or role
        - Keywords in message ("ai agents", "enterprise", "automation", "custom", "urgent", "budget")
        """
        score = 40  # baseline
        email = lead.get("email", "").strip().lower()
        name = lead.get("name", "").strip()
        company = lead.get("company", "").strip()
        message = lead.get("message", "").strip().lower()

        free_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "university.edu"]
        domain = email.split("@")[-1] if "@" in email else ""
        
        if domain and domain not in free_domains and not domain.endswith(".edu") and not domain.endswith(".gov"):
            score += 25
        elif domain.endswith(".gov"):
            score += 15

        # Title / Role indicators
        exec_titles = ["ceo", "cto", "vp", "founder", "director", "head", "owner", "president"]
        if any(t in name.lower() or t in message for t in exec_titles):
            score += 20

        # Keyword matching
        high_value_keywords = ["ai agents", "enterprise", "automation", "custom", "urgent", "budget", "sales", "agents", "scale", "workflow"]
        matches = sum(1 for kw in high_value_keywords if kw in message)
        score += min(matches * 10, 40)

        # Cap score at 100
        score = min(score, 100)

        # Determine tier
        if score >= 80:
            tier = "High-Intent"
        elif score >= 60:
            tier = "Medium-Intent"
        else:
            tier = "Nurture"

        scored_lead = dict(lead)
        scored_lead["score"] = score
        scored_lead["tier"] = tier
        scored_lead["triaged_at"] = datetime.now().isoformat()
        return scored_lead

    def draft_outreach_email(self, scored_lead: dict) -> dict:
        """
        Drafts a personalized sales outreach email based on lead triage data.
        """
        name = scored_lead.get("name", "there")
        company = scored_lead.get("company", "your organization")
        tier = scored_lead.get("tier", "Standard")

        subject = f"Custom AI Agents & Enterprise Automation for {company}"
        body = (
            f"Hi {name},\n\n"
            f"We noticed your interest in scaling {company} with autonomous AI agents and automated workflows.\n"
            f"Our enterprise agent roster is designed to deploy high-impact AI solutions tailored specifically to your pipeline.\n\n"
            f"Would you be open to a brief 10-minute discovery call this week to review a custom rollout plan?\n\n"
            f"Best regards,\n"
            f"Autonomous Enterprise Sales Team"
        )

        return {
            "recipient": scored_lead.get("email"),
            "subject": subject,
            "body": body,
            "tier": tier,
            "status": "drafted"
        }

    def sync_to_crm(self, lead: dict) -> dict:
        """
        Synchronizes the lead record into the database CRM table.
        """
        conn = get_db_connection(self.db_path)
        try:
            name = lead.get("name", "Unknown")
            email = lead.get("email", "")
            company = lead.get("company", "")
            status = lead.get("tier", "New")
            save_lead(conn, name, email, company, status)
            log_agent_action(conn, "LeadTriageEngine", "SyncToCRM", "Success", f"Synced lead {email} to CRM")
        finally:
            conn.close()

        return {
            "status": "synced",
            "email": lead.get("email")
        }

def run_lead_triage_cycle(leads: list = None, dry_run: bool = True, db_path: str = None) -> dict:
    """
    Executes a complete lead triage and sales outreach cycle:
    1. Ingestion / loading of leads
    2. Scoring and tiering
    3. CRM synchronization
    4. Outreach drafting for high-intent leads
    """
    engine = LeadTriageEngine(dry_run=dry_run, db_path=db_path)
    if leads is None:
        leads = [
            {"email": "exec@enterprise.com", "name": "Exec Lead", "company": "Enterprise Inc", "message": "Looking for custom AI agents and enterprise automation setup."}
        ]

    processed = 0
    high_intent_count = 0
    outbox = []

    for lead in leads:
        scored = engine.score_and_triage(lead)
        processed += 1
        engine.sync_to_crm(scored)

        if scored["tier"] == "High-Intent":
            high_intent_count += 1
            draft = engine.draft_outreach_email(scored)
            outbox.append(draft)

    conn = get_db_connection(db_path)
    try:
        log_agent_action(conn, "LeadTriageEngine", "TriageCycle", "Success", f"Processed {processed} leads, {high_intent_count} high-intent.")
    finally:
        conn.close()

    return {
        "processed": processed,
        "high_intent_count": high_intent_count,
        "outbox": outbox,
        "status": "completed"
    }
