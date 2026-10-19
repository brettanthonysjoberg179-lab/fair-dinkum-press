# Australian Online Business Practices Lawyer Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust, Python-based Australian Online Business Practices Lawyer Agent that audits websites, terms, refund policies, pricing, and marketing for compliance with Australian Consumer Law (ACL), the Privacy Act 1988 (including APPs), and the Spam Act 2003.

**Architecture:** A modular Python CLI and programmatic script (`scripts/agentkit/au_legal_compliance_agent.py`) that parses target website URLs or Markdown legal documents, evaluates them against strict statutory rules, and outputs a structured JSON report and human-readable compliance scorecard.

**Tech Stack:** Python 3.13, BeautifulSoup4 / httpx (for web scraping and inspection), pytest (for validation tests).

**Spec:** Designed in conversation with the user (ACL, Privacy Act 1988 / APPs, Spam Act 2003, and Automated Audit CLI).

## Global Constraints

- Must strictly adhere to Australian Consumer Law (Schedule 2 of the Competition and Consumer Act 2010).
- Must verify Privacy Act 1988 (Cth) and Australian Privacy Principles (APPs 1–13).
- Must check Spam Act 2003 compliance for electronic marketing.
- Python code must be fully typed and tested.

## Review Focus

1. **Missing Refund Policy / Unlawful "No Refunds" Clauses:** ACL guarantees cannot be excluded. The agent must flag absolute "no refunds" statements.
2. **GST-Inclusive Pricing:** Consumer prices must be displayed inclusive of GST under ACL section 48.
3. **Offshore Data Storage Disclosures:** Privacy Act / APP 8 cross-border disclosure requirements.
4. **Consent & Unsubscribe Mechanisms:** Spam Act 2003 express/inferred consent and clear unsubscribe links.
5. **Robust Error Handling:** Graceful fallback if target URL is unreachable or invalid.

---

### Task 1: Core Compliance Rule Engine & Data Structures

**Files:**
- Create: `scripts/agentkit/au_legal_compliance_agent.py`
- Test: `tests/test_au_legal_compliance.py`

**Interfaces:**
- Produces: `ComplianceAuditor` class and rule evaluation functions.

- [ ] **Step 1: Write the failing test for ACL refund policy evaluation**

```python
import pytest
from scripts.agentkit.au_legal_compliance_agent import ComplianceAuditor

def test_audit_refund_policy_violation():
    auditor = ComplianceAuditor()
    text = "All sales are final. No refunds under any circumstances."
    result = auditor.audit_refund_policy(text)
    assert result["compliant"] is False
    assert "no refunds" in result["violation"].lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_au_legal_compliance.py -v`
Expected: FAIL with ModuleNotFoundError or AttributeError

- [ ] **Step 3: Implement `ComplianceAuditor` in `scripts/agentkit/au_legal_compliance_agent.py`**

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_au_legal_compliance.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_au_legal_compliance.py scripts/agentkit/au_legal_compliance_agent.py
git commit -m "feat: add ComplianceAuditor class with ACL refund policy checks"
```

---

### Task 2: Privacy Act & Spam Act Evaluation Rules

**Files:**
- Modify: `scripts/agentkit/au_legal_compliance_agent.py`
- Modify: `tests/test_au_legal_compliance.py`

**Interfaces:**
- Consumes: `ComplianceAuditor` from Task 1.
- Produces: Privacy Policy (APP) and Spam Act 2003 audit methods.

- [ ] **Step 1: Write the failing test for Privacy Act & Spam Act checks**

```python
def test_audit_privacy_and_spam():
    auditor = ComplianceAuditor()
    privacy_text = "We collect your data and store it offshore without notifying you."
    spam_text = "Buy now! No unsubscribe link provided."
    
    priv_res = auditor.audit_privacy_policy(privacy_text)
    spam_res = auditor.audit_spam_act(spam_text)
    
    assert priv_res["compliant"] is False
    assert spam_res["compliant"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_au_legal_compliance.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `audit_privacy_policy` and `audit_spam_act` in `scripts/agentkit/au_legal_compliance_agent.py`**

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_au_legal_compliance.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_au_legal_compliance.py scripts/agentkit/au_legal_compliance_agent.py
git commit -m "feat: add Privacy Act APP and Spam Act 2003 audit rules"
```

---

### Task 3: CLI & Report Generation

**Files:**
- Modify: `scripts/agentkit/au_legal_compliance_agent.py`
- Modify: `tests/test_au_legal_compliance.py`

**Interfaces:**
- Consumes: Full `ComplianceAuditor` functionality.
- Produces: CLI argument parser and JSON/Markdown report output.

- [ ] **Step 1: Write the failing test for CLI report generation**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_au_legal_compliance.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `generate_comprehensive_report` and CLI entrypoint in `scripts/agentkit/au_legal_compliance_agent.py`**

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_au_legal_compliance.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_au_legal_compliance.py scripts/agentkit/au_legal_compliance_agent.py
git commit -m "feat: add comprehensive report generation and CLI support for lawyer agent"
```
