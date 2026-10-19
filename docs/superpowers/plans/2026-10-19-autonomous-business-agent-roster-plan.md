# Autonomous Enterprise Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a 99% autonomous annual business engine (June 1 – May 31) featuring 24/7 agent rosters for digital publishing, lead triage, and micro-SaaS operations, integrated with a Gmail-based Human-In-The-Loop (HITL) communication and approval bus.

**Architecture:** Python 3.11+ asynchronous application using APScheduler for 24/7 agent scheduling, SQLite + RAGS Vector Memory DB for state persistence, and Gmail API integration via Composio/Google OAuth for bi-directional HITL communication and command parsing.

**Tech Stack:** Python, `asyncio`, `apscheduler`, `google-api-python-client`, `sqlite3`, `fastapi`, `pydantic`.

**Spec:** `docs/superpowers/specs/2026-10-19-autonomous-business-agent-roster-design.md`

## Global Constraints

- Python 3.11+ compatibility.
- Environment secrets (`GMAIL_API_KEY`, `STRIPE_API_KEY`, `COMPOSIO_API_KEY`) loaded securely from `.env` without hardcoding.
- All agent actions must log to SQLite and emit Gmail notifications for high-risk actions.
- Annual reset mechanism triggers on June 1.

## Review Focus

1. **Gmail Authentication & Rate Limits:** Ensure exponential backoff and robust error handling when polling Gmail API.
2. **Agent Race Conditions:** Prevent overlapping scheduled task executions across the 24/7 roster.
3. **HITL Command Injection / Spoofing:** Validate sender email addresses against authorized admin whitelist before processing commands.
4. **Stripe Webhook Verification:** Secure incoming micro-SaaS webhook signatures against tampering.
5. **Database Locking:** Use WAL mode in SQLite for safe concurrent writes by multi-agent workers.

---

### Task 1: State Manager & Database Schema

**Files:**
- Create: `scripts/autonomous/database.py`
- Test: `tests/test_autonomous_database.py`

**Interfaces:**
- Consumes: None
- Produces: `init_db()`, `get_db_connection()`, `log_agent_action()`, `save_lead()`, `save_content_record()`

- [ ] **Step 1: Write failing test for database initialization and record logging**

```python
import os
import sqlite3
import pytest
from scripts.autonomous.database import init_db, get_db_connection, log_agent_action

def test_database_init_and_logging(tmp_path):
    db_path = tmp_path / "test_business.db"
    conn = init_db(str(db_path))
    assert conn is not None
    
    log_agent_action(conn, "PublishingAgent", "KeywordScrape", "Success", "Found 5 new keywords")
    cursor = conn.cursor()
    cursor.execute("SELECT agent, action, status FROM agent_logs")
    row = cursor.fetchone()
    assert row == ("PublishingAgent", "KeywordScrape", "Success")
    conn.close()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_autonomous_database.py -v`
Expected: FAIL with ModuleNotFoundError or sqlite error

- [ ] **Step 3: Implement `database.py` in `scripts/autonomous/`**

Create SQLite schema with tables for `agent_logs`, `leads`, `content_records`, and `saas_metrics` with WAL mode enabled.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_autonomous_database.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/autonomous/database.py tests/test_autonomous_database.py
git commit -m "feat: add autonomous enterprise database and logging manager"
```

---

### Task 2: Gmail HITL Gateway & Command Bus

**Files:**
- Create: `scripts/autonomous/gmail_hitl.py`
- Test: `tests/test_gmail_hitl.py`

**Interfaces:**
- Consumes: `database.py`
- Produces: `GmailHITLGateway`, `poll_inbox_for_commands()`, `send_approval_request()`, `send_morning_digest()`

- [ ] **Step 1: Write failing test for email command parsing and sender authorization**

```python
import pytest
from scripts.autonomous.gmail_hitl import GmailHITLGateway

def test_command_parsing():
    gateway = GmailHITLGateway(admin_email="admin@fairdinkum.press", dry_run=True)
    msg = {
        "sender": "admin@fairdinkum.press",
        "subject": "[PublishingAgent] Command: Draft blog post about AI agents",
        "body": "Please draft an article on autonomous workflows."
    }
    parsed = gateway.parse_incoming_message(msg)
    assert parsed["authorized"] is True
    assert parsed["agent"] == "PublishingAgent"
    assert parsed["command"] == "Draft blog post about AI agents"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_gmail_hitl.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement `gmail_hitl.py`**

Implement `GmailHITLGateway` supporting Gmail API client integration, sender whitelist validation, approval thread management, and automated morning digest dispatch.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_gmail_hitl.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/autonomous/gmail_hitl.py tests/test_gmail_hitl.py
git commit -m "feat: add Gmail HITL gateway and command bus"
```

---

### Task 3: Pillar A - Automated Digital Publishing Engine

**Files:**
- Create: `scripts/autonomous/publishing_engine.py`
- Test: `tests/test_publishing_engine.py`

**Interfaces:**
- Consumes: `database.py`, `gmail_hitl.py`
- Produces: `PublishingEngine`, `run_publishing_cycle()`

- [ ] **Step 1: Write failing test for publishing cycle execution**

```python
import pytest
from scripts.autonomous.publishing_engine import PublishingEngine

def test_publishing_cycle(tmp_path):
    engine = PublishingEngine(dry_run=True)
    result = engine.execute_cycle()
    assert result["status"] == "success"
    assert "article_title" in result
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_publishing_engine.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement `publishing_engine.py`**

Implement keyword discovery, markdown content generation, Nano Banana asset integration stub, and publishing pipeline.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_publishing_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/autonomous/publishing_engine.py tests/test_publishing_engine.py
git commit -m "feat: add Pillar A automated digital publishing engine"
```

---

### Task 4: Pillar B - Client Lead Triage & Sales Outreach

**Files:**
- Create: `scripts/autonomous/lead_triage.py`
- Test: `tests/test_lead_triage.py`

**Interfaces:**
- Consumes: `database.py`, `gmail_hitl.py`
- Produces: `LeadTriageEngine`, `run_lead_triage_cycle()`

- [ ] **Step 1: Write failing test for lead triage and scoring**

```python
import pytest
from scripts.autonomous.lead_triage import LeadTriageEngine

def test_lead_scoring():
    engine = LeadTriageEngine(dry_run=True)
    lead = {"email": "ceo@enterprise.com", "message": "Interested in custom AI agents and enterprise automation setup."}
    scored = engine.score_and_triage(lead)
    assert scored["score"] >= 80
    assert scored["tier"] == "High-Intent"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_lead_triage.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement `lead_triage.py`**

Implement inbound message parsing, ICP scoring algorithm, outreach drafting, and CRM sync integration.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_lead_triage.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/autonomous/lead_triage.py tests/test_lead_triage.py
git commit -m "feat: add Pillar B client lead triage and sales outreach engine"
```

---

### Task 5: Pillar C - Micro-SaaS Operations & Self-Healing Worker

**Files:**
- Create: `scripts/autonomous/saas_operations.py`
- Test: `tests/test_saas_operations.py`

**Interfaces:**
- Consumes: `database.py`, `gmail_hitl.py`
- Produces: `SaaSOperationsEngine`, `run_saas_health_check()`

- [ ] **Step 1: Write failing test for SaaS health check and error handling**

```python
import pytest
from scripts.autonomous.saas_operations import SaaSOperationsEngine

def test_health_check():
    engine = SaaSOperationsEngine(dry_run=True)
    report = engine.run_health_check()
    assert report["status"] == "healthy"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_saas_operations.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement `saas_operations.py`**

Implement endpoint uptime monitoring, Stripe webhook event handler simulation, and self-healing diagnostic logger.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_saas_operations.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/autonomous/saas_operations.py tests/test_saas_operations.py
git commit -m "feat: add Pillar C micro-saas operations and self-healing worker"
```

---

### Task 6: 24/7 APScheduler Roster & Annual June 1 Reset

**Files:**
- Create: `scripts/autonomous/scheduler_roster.py`
- Test: `tests/test_scheduler_roster.py`

**Interfaces:**
- Consumes: `database.py`, `gmail_hitl.py`, `publishing_engine.py`, `lead_triage.py`, `saas_operations.py`
- Produces: `AutonomousEnterpriseOrchestrator`, `main()`

- [ ] **Step 1: Write failing test for scheduler initialization and June 1 check**

```python
import pytest
from datetime import datetime
from scripts.autonomous.scheduler_roster import AutonomousEnterpriseOrchestrator

def test_june_first_reset_check():
    orch = AutonomousEnterpriseOrchestrator(dry_run=True)
    # Test June 1 trigger logic
    june_1 = datetime(2027, 6, 1, 0, 0, 0)
    assert orch.is_annual_kickoff(june_1) is True
    
    other_date = datetime(2027, 10, 19, 0, 0, 0)
    assert orch.is_annual_kickoff(other_date) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_scheduler_roster.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement `scheduler_roster.py`**

Implement APScheduler async loop connecting all three pillars, Gmail polling cron, daily 06:00 UTC digest, and June 1 annual reset protocol.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_scheduler_roster.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/autonomous/scheduler_roster.py tests/test_scheduler_roster.py
git commit -m "feat: add 24/7 APScheduler roster and June 1 annual reset workflow"
```
