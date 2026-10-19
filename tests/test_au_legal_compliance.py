import pytest
from scripts.agentkit.au_legal_compliance_agent import ComplianceAuditor, AULegalComplianceAgent

def test_audit_refund_policy_violation():
    auditor = ComplianceAuditor()
    text = "All sales are final. No refunds under any circumstances."
    result = auditor.audit_refund_policy(text)
    assert result["compliant"] is False
    assert "no refunds" in result["violation"].lower()

def test_audit_privacy_and_spam():
    auditor = ComplianceAuditor()
    privacy_text = "We collect your data and store it offshore without notifying you."
    spam_text = "Buy now! No unsubscribe link provided."
    
    priv_res = auditor.audit_privacy_policy(privacy_text)
    spam_res = auditor.audit_spam_act(spam_text)
    
    assert priv_res["compliant"] is False
    assert spam_res["compliant"] is False

def test_generate_audit_report(tmp_path):
    auditor = ComplianceAuditor()
    sample_data = {
        "refund_text": "No refunds.",
        "privacy_text": "We store data abroad.",
        "spam_text": "No opt out."
    }
    report = auditor.generate_comprehensive_report(sample_data)
    assert "score" in report
    assert "violations" in report
