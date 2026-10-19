# Greeting Email Service Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a warm and professional personalized greeting email service supporting Birthdays, Christmas, Easter, Valentine's Day, and Halloween with SQLite contact storage and automated scheduling.

**Architecture:** Python application with SQLite backend, OCCASION_TEMPLATES dictionary for warm/professional messaging, and dispatcher daemon.

**Tech Stack:** Python, `sqlite3`, `pytest`.

**Spec:** `docs/superpowers/specs/2026-10-19-greeting-email-service-design.md`

## Global Constraints
- Python 3.11+ compatibility.
- Warm and professional tone across all 5 occasion templates.

---

### Task 1: Database & Contact Manager

**Files:**
- Create: `scripts/greetings/db.py`
- Test: `tests/test_greeting_db.py`

**Interfaces:**
- Consumes: None
- Produces: `init_greeting_db()`, `add_contact()`, `get_contacts_for_birthday()`

- [ ] **Step 1: Write failing test for contact database and birthday lookup**

```python
import pytest
from scripts.greetings.db import init_greeting_db, add_contact, get_contacts_by_birthday

def test_greeting_db(tmp_path):
    db_path = tmp_path / "greetings.db"
    conn = init_greeting_db(str(db_path))
    add_contact(conn, "Jane Doe", "jane@example.com", "10-19", "Colleague")
    contacts = get_contacts_by_birthday(conn, "10-19")
    assert len(contacts) == 1
    assert contacts[0]["name"] == "Jane Doe"
    conn.close()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=. pytest tests/test_greeting_db.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `scripts/greetings/db.py`**

Create SQLite tables for `contacts` and `dispatch_logs` and CRUD helpers.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=. pytest tests/test_greeting_db.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/greetings/db.py tests/test_greeting_db.py
git commit -m "feat: add greeting service db and contact manager"
```

---

### Task 2: Occasion Templates & Dispatcher

**Files:**
- Create: `scripts/greetings/dispatcher.py`
- Test: `tests/test_greeting_dispatcher.py`

**Interfaces:**
- Consumes: `db.py`
- Produces: `render_greeting_email()`, `dispatch_greeting()`

- [ ] **Step 1: Write failing test for email template rendering**

```python
import pytest
from scripts.greetings.dispatcher import render_greeting_email

def test_template_rendering():
    email = render_greeting_email("birthday", "Jane", "Alice", "Great colleague")
    assert "Jane" in email["subject"]
    assert "Alice" in email["body"]
    assert "professional" in email["body"].lower() or "success" in email["body"].lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=. pytest tests/test_greeting_dispatcher.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `scripts/greetings/dispatcher.py`**

Define warm and professional templates for birthday, christmas, easter, valentines, and halloween.

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=. pytest tests/test_greeting_dispatcher.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/greetings/dispatcher.py tests/test_greeting_dispatcher.py
git commit -m "feat: add greeting email templates and dispatcher"
```
