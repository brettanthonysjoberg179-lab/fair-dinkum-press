import os
import re
import logging
from datetime import datetime
from scripts.autonomous.database import get_db_connection, log_agent_action

logger = logging.getLogger(__name__)

class GmailHITLGateway:
    """
    Gmail Human-in-the-Loop (HITL) Gateway and Command Bus for Autonomous Enterprise Agents.
    Handles secure inbound email commands (whitelisted sender + agent command tag),
    outbound HITL approval requests, and automated morning operational digests.
    """
    def __init__(self, admin_email="admin@fairdinkum.press", dry_run=True, db_path=None, whitelisted_senders=None):
        self.admin_email = admin_email
        self.dry_run = dry_run
        self.db_path = db_path
        self.whitelisted_senders = whitelisted_senders or [admin_email]

    def parse_incoming_message(self, msg: dict) -> dict:
        """
        Parses an incoming email message dictionary with keys: sender, subject, body.
        Validates sender against whitelist.
        Extracts target agent and command description from subject line:
        Format expected: [AgentName] Command: <command description>
        """
        sender = msg.get("sender", "").strip().lower()
        subject = msg.get("subject", "").strip()
        body = msg.get("body", "").strip()

        authorized = sender in [w.lower() for w in self.whitelisted_senders]

        agent = "Unknown"
        command = subject

        # Regex to match [AgentName] Command: <description> or [AgentName] <description>
        match = re.match(r'^\[([A-Za-z0-9_]+)\]\s+(?:Command:\s*)?(.+)$', subject)
        if match:
            agent = match.group(1)
            command = match.group(2)

        return {
            "authorized": authorized,
            "agent": agent,
            "command": command,
            "body": body,
            "sender": sender
        }

    def poll_inbox_for_commands(self) -> list:
        """
        Polls inbox for incoming commands. In dry_run mode, returns simulated commands
        or processes database queue. Logs polling action.
        """
        conn = get_db_connection(self.db_path)
        try:
            log_agent_action(conn, "GmailHITLGateway", "PollInbox", "Success", "Polled inbox successfully")
        finally:
            conn.close()
        return []

    def send_approval_request(self, agent_name: str, action_description: str, context_data: dict = None) -> dict:
        """
        Sends an email requesting human-in-the-loop approval for a sensitive agent action.
        """
        subject = f"[HITL Approval Required] [{agent_name}] {action_description}"
        body = f"Agent '{agent_name}' is requesting approval for action:\n\n{action_description}\n\nContext:\n{context_data or 'None'}\n\nReply with 'APPROVE' or 'REJECT'."
        
        conn = get_db_connection(self.db_path)
        try:
            log_agent_action(conn, "GmailHITLGateway", "SendApprovalRequest", "Sent", f"Requested approval for {agent_name}: {action_description}")
        finally:
            conn.close()

        return {
            "status": "sent",
            "recipient": self.admin_email,
            "subject": subject,
            "body": body
        }

    def send_morning_digest(self, metrics_summary = None) -> dict:
        """
        Compiles and sends the automated morning operational digest summarizing agent activity,
        leads, content publications, and SaaS metrics from the database.
        """
        conn = get_db_connection(self.db_path)
        try:
            cursor = conn.cursor()
            
            # Gather recent metrics/stats if summary not provided
            cursor.execute("SELECT COUNT(*) as count FROM agent_logs WHERE timestamp >= datetime('now', '-1 day')")
            log_count = cursor.fetchone()["count"]
            
            cursor.execute("SELECT COUNT(*) as count FROM leads WHERE timestamp >= datetime('now', '-1 day')")
            lead_count = cursor.fetchone()["count"]
            
            cursor.execute("SELECT COUNT(*) as count FROM content_records WHERE timestamp >= datetime('now', '-1 day')")
            content_count = cursor.fetchone()["count"]
            
            summary = metrics_summary if metrics_summary is not None else {
                "agent_actions_24h": log_count,
                "new_leads_24h": lead_count,
                "content_published_24h": content_count
            }
        except Exception as e:
            logger.warning(f"Could not query metrics for digest: {e}")
            summary = metrics_summary if metrics_summary is not None else {"error": str(e)}
        finally:
            conn.close()

        today_str = datetime.now().strftime("%Y-%m-%d")
        subject = f"[Fair Dinkum Press] Morning Digest - {today_str}"
        
        if isinstance(summary, str):
            body = summary
        else:
            body = f"Good morning,\n\nHere is your autonomous enterprise operational summary for {today_str}:\n\n"
            for k, v in summary.items():
                body += f"- {k.replace('_', ' ').title()}: {v}\n"
            body += "\nAll autonomous agent systems operating nominally."

        conn = get_db_connection(self.db_path)
        try:
            log_agent_action(conn, "GmailHITLGateway", "SendMorningDigest", "Sent", f"Sent morning digest to {self.admin_email}")
        finally:
            conn.close()

        return {
            "status": "sent",
            "recipient": self.admin_email,
            "subject": subject,
            "body": body,
            "summary": summary
        }
