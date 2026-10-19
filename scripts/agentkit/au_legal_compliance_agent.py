#!/usr/bin/env python3
"""
AU Legal Compliance Agent — Autonomous AI Compliance & Audit Tool
================================================================
An expert legal compliance agent designed for Australian businesses, fintechs,
and solopreneurs to audit codebases, inspect data flows, verify Privacy Act
APP 1.7 automated decision-making compliance, and generate executive audit reports.

Tools Included:
    1. ComplianceAuditor: Evaluates text/policies against ACL, Privacy Act, and Spam Act.
    2. scan_codebase_for_pii_and_privacy: Scans project files for unencrypted PII or missing privacy notices.
    3. audit_app17_automated_decisions: Verifies automated scoring/lending workflows for disclosure registers and human review mechanisms.
    4. inspect_api_data_flows: Reviews API endpoints and database schemas for secure data handling.
    5. generate_compliance_report: Compiles findings into an executive audit report.
    6. dispatch_compliance_alert: Sends alerts via Gmail / Slack (Composio) when risks are identified.

Usage:
    python au_legal_compliance_agent.py --scan
    python au_legal_compliance_agent.py --audit --target .
    python au_legal_compliance_agent.py --dry-run
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Setup logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
REPORTS_DIR = Path("docs/compliance")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "compliance_agent.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("au-legal-compliance-agent")

COMPOSIO_CLI = "/home/brettanthonysjoberg179/.local/bin/composio"

class ComplianceAuditor:
    """Evaluates legal texts against Australian Consumer Law (ACL), Privacy Act 1988 (APPs), and Spam Act 2003."""
    
    def audit_refund_policy(self, text: str) -> dict:
        text_lower = text.lower()
        violations = []
        no_refund_phrases = ["no refunds", "all sales final", "non-refundable under any circumstances", "no refund", "final sale"]
        for phrase in no_refund_phrases:
            if phrase in text_lower:
                violations.append(f"Unlawful 'no refunds' clause detected: '{phrase}' violates Australian Consumer Law (ACL) statutory guarantees.")
        
        if violations:
            return {"compliant": False, "violation": "; ".join(violations), "details": violations}
        return {"compliant": True, "violation": None, "details": []}

    def audit_privacy_policy(self, text: str) -> dict:
        text_lower = text.lower()
        violations = []
        if "offshore" in text_lower or "abroad" in text_lower or "overseas" in text_lower:
            negative_indicators = ["without notifying", "without notice", "without consent", "no notification", "no consent", "without disclosure"]
            has_negative = any(neg in text_lower for neg in negative_indicators)
            
            has_consent = "consent" in text_lower and not "without consent" in text_lower
            has_disclosure = ("disclosure" in text_lower or "disclose" in text_lower) and not "without disclosure" in text_lower
            
            if has_negative or not (has_consent or has_disclosure):
                violations.append("Privacy Act APP 8 cross-border disclosure violation: offshore data storage mentioned without adequate disclosure or consent notice.")
        
        if violations:
            return {"compliant": False, "violation": "; ".join(violations), "details": violations}
        return {"compliant": True, "violation": None, "details": []}

    def audit_spam_act(self, text: str) -> dict:
        text_lower = text.lower()
        violations = []
        no_unsubscribe_phrases = ["no unsubscribe", "without unsubscribe", "no opt-out", "without opt-out", "no opt out", "without opt out", "no unsubscribe link"]
        has_no_unsubscribe = any(phrase in text_lower for phrase in no_unsubscribe_phrases)
        
        has_unsubscribe = ("unsubscribe" in text_lower and not has_no_unsubscribe) or ("opt-out" in text_lower and "no opt-out" not in text_lower) or ("opt out" in text_lower and "no opt out" not in text_lower)
        
        if "marketing" in text_lower or "promot" in text_lower or "buy" in text_lower or "offer" in text_lower or "now!" in text_lower:
            if not has_unsubscribe or has_no_unsubscribe:
                violations.append("Spam Act 2003 violation: commercial electronic message lacks clear unsubscribe or opt-out mechanism.")
        
        if violations:
            return {"compliant": False, "violation": "; ".join(violations), "details": violations}
        return {"compliant": True, "violation": None, "details": []}

    def generate_comprehensive_report(self, audit_data: dict) -> dict:
        refund_text = audit_data.get("refund_text", "")
        privacy_text = audit_data.get("privacy_text", "")
        spam_text = audit_data.get("spam_text", "")

        refund_res = self.audit_refund_policy(refund_text)
        privacy_res = self.audit_privacy_policy(privacy_text)
        spam_res = self.audit_spam_act(spam_text)

        violations = []
        if not refund_res["compliant"]:
            violations.append(refund_res["violation"])
        if not privacy_res["compliant"]:
            violations.append(privacy_res["violation"])
        if not spam_res["compliant"]:
            violations.append(spam_res["violation"])

        score = max(0, 100 - (len(violations) * 33))

        return {
            "score": score,
            "violations": violations,
            "refund_audit": refund_res,
            "privacy_audit": privacy_res,
            "spam_audit": spam_res,
            "timestamp": datetime.now().isoformat()
        }


class AULegalComplianceAgent:
    def __init__(self, target_dir: str = ".", dry_run: bool = True):
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run
        self.findings = []
        self.auditor = ComplianceAuditor()

    def execute_composio(self, tool_slug: str, params: dict) -> dict:
        """Executes external tool calls via Composio CLI."""
        if self.dry_run:
            log.info("[DRY RUN] Would execute Composio tool: %s with params: %s", tool_slug, params)
            return {"status": "dry_run_success", "tool": tool_slug}
        
        cmd = [COMPOSIO_CLI, "execute", tool_slug, "-d", json.dumps(params)]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if res.returncode != 0:
                return {"error": res.stderr or res.stdout}
            out = res.stdout
            start = out.find('{')
            end = out.rfind('}')
            if start != -1 and end != -1:
                return json.loads(out[start:end+1])
            return {"raw": out}
        except Exception as e:
            return {"error": str(e)}

    def tool_scan_codebase_for_pii(self) -> dict:
        """Tool 1: Scans codebase for unencrypted PII collection, logging of sensitive data, or missing privacy policies."""
        log.info("🔍 Running Tool: scan_codebase_for_pii on %s...", self.target_dir)
        suspicious_patterns = ["password", "credit_card", "ssn", "tfn", "driver_license", "raw_pii", "plain_token"]
        matches = []

        for p in self.target_dir.rglob("*"):
            if p.is_file() and p.suffix in [".py", ".js", ".ts", ".json", ".md", ".env"]:
                if any(ignored in str(p) for ignored in [".git", "__pycache__", ".venv", "node_modules"]):
                    continue
                try:
                    content = p.read_text(errors="ignore")
                    for pattern in suspicious_patterns:
                        if pattern in content.lower():
                            matches.append({"file": str(p), "pattern_matched": pattern})
                except Exception:
                    pass

        finding = {
            "tool": "scan_codebase_for_pii",
            "status": "completed",
            "matches_found": len(matches),
            "details": matches[:10]  # limit sample
        }
        self.findings.append(finding)
        return finding

    def tool_audit_app17_automated_decisions(self) -> dict:
        """Tool 2: Audits automated scoring/lending workflows for Privacy Act APP 1.7 compliance (disclosure + human review)."""
        log.info("⚖️ Running Tool: audit_app17_automated_decisions...")
        
        decision_scripts = list(self.target_dir.glob("**/*triage*")) + list(self.target_dir.glob("**/*score*")) + list(self.target_dir.glob("**/*predict*"))
        
        compliance_gaps = []
        for script in decision_scripts:
            if any(ignored in str(script) for ignored in [".git", "__pycache__", ".venv", "node_modules"]):
                continue
            try:
                code = script.read_text(errors="ignore")
                has_disclosure = "disclosure" in code.lower() or "privacy" in code.lower() or "app 1.7" in code.lower()
                has_human_review = "human" in code.lower() or "review" in code.lower() or "manual" in code.lower()
                
                if not (has_disclosure and has_human_review):
                    compliance_gaps.append({
                        "file": str(script),
                        "missing_disclosure": not has_disclosure,
                        "missing_human_review": not has_human_review
                    })
            except Exception:
                pass

        finding = {
            "tool": "audit_app17_automated_decisions",
            "status": "completed",
            "compliance_gaps_count": len(compliance_gaps),
            "details": compliance_gaps
        }
        self.findings.append(finding)
        return finding

    def tool_inspect_api_data_flows(self) -> dict:
        """Tool 3: Inspects API endpoints and database schemas for secure data handling and encryption standards."""
        log.info("🔒 Running Tool: inspect_api_data_flows...")
        
        db_files = list(self.target_dir.glob("**/*.sql")) + list(self.target_dir.glob("**/*.db"))
        schema_issues = []
        
        for db in db_files:
            if any(ignored in str(db) for ignored in [".git", "__pycache__", ".venv", "node_modules"]):
                continue
            try:
                content = db.read_text(errors="ignore")
                if "encrypt" not in content.lower() and "hash" not in content.lower():
                    schema_issues.append({"file": str(db), "note": "Database schema lacks explicit encryption/hashing indicators for sensitive columns."})
            except Exception:
                pass

        finding = {
            "tool": "inspect_api_data_flows",
            "status": "completed",
            "schema_issues_count": len(schema_issues),
            "details": schema_issues
        }
        self.findings.append(finding)
        return finding

    def tool_generate_compliance_report(self) -> str:
        """Tool 4: Compiles all audit findings into an executive compliance report."""
        log.info("📝 Running Tool: generate_compliance_report...")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report_lines = [
            f"# 🛡️ AU Legal Compliance & Privacy Act Audit Report",
            f"**Generated:** {timestamp}",
            f"**Target Directory:** `{self.target_dir.absolute()}`",
            f"**Jurisdiction:** Australia (Federal Privacy Act 1988, APP 1.7)",
            f"",
            f"---",
            f"",
            f"## 📊 Executive Summary",
            f"This automated audit report evaluates codebase security, PII handling, and automated decision-making (APP 1.7) compliance across the Fair Dinkum workspace.",
            f"",
            f"## 🔍 Audit Findings",
            f""
        ]

        for finding in self.findings:
            report_lines.append(f"### Tool: `{finding['tool']}`")
            report_lines.append(f"- **Status:** {finding['status']}")
            report_lines.append(f"- **Summary Data:** `{json.dumps(finding, indent=2)}`")
            report_lines.append(f"")

        report_lines.extend([
            f"---",
            f"## ✅ Recommended Corrective Actions",
            f"1. **APP 1.7 Compliance:** Ensure all automated scoring and triage scripts include clear public disclosures and human review pathways.",
            f"2. **PII Protection:** Verify that all sensitive tokens and identifiers are securely hashed or encrypted.",
            f"3. **Regular Audits:** Run `au_legal_compliance_agent.py --audit` weekly to maintain continuous compliance posture.",
            f""
        ])

        report_content = "\n".join(report_lines)
        report_path = REPORTS_DIR / f"compliance_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report_content)
        log.info("📄 Compliance report saved to %s", report_path)
        return str(report_path)

    def tool_dispatch_alert(self, report_path: str) -> dict:
        """Tool 5: Dispatches compliance notification via Composio Gmail / Slack tools."""
        log.info("📢 Running Tool: dispatch_compliance_alert...")
        payload = {
            "recipient": "admin@fairdinkum.press",
            "subject": "[Compliance Alert] AU Legal Compliance Audit Completed",
            "body": f"Compliance audit successfully completed. Report generated at: {report_path}. Please review attached findings for APP 1.7 and PII compliance."
        }
        res = self.execute_composio("GMAIL_SEND_EMAIL", payload)
        return res

    def run_full_audit(self):
        log.info("🚀 Starting AU Legal Compliance Agent Full Audit Suite...")
        self.tool_scan_codebase_for_pii()
        self.tool_audit_app17_automated_decisions()
        self.tool_inspect_api_data_flows()
        report_path = self.tool_generate_compliance_report()
        alert_res = self.tool_dispatch_alert(report_path)
        log.info("✨ Compliance Audit Suite completed successfully! Report: %s", report_path)

def main():
    parser = argparse.ArgumentParser(description="AU Legal Compliance Agent")
    parser.add_argument("--scan", action="store_true", help="Run codebase PII scan")
    parser.add_argument("--audit", action="store_true", help="Run full compliance audit suite (APP 1.7 + PII + Data Flows)")
    parser.add_argument("--target", default=".", help="Target directory to audit")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Run in dry-run mode (default)")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Run in live mode (executes real API calls)")

    args = parser.parse_args()

    agent = AULegalComplianceAgent(target_dir=args.target, dry_run=args.dry_run)

    if args.scan:
        agent.tool_scan_codebase_for_pii()
        agent.tool_generate_compliance_report()
    elif args.audit:
        agent.run_full_audit()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
