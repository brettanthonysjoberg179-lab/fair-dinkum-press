# FormFav Subscription Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 100% automate the daily FormFav racing intelligence pipeline, trifecta prediction generation, booklet compilation, and subscriber distribution on a recurring subscription model.

**Architecture:** 
1. **Automation Daemon / Cron:** A scheduled background job executing `daily_formfav_fetch.sh` every morning at 04:00 AM AEST/AEDT.
2. **Prediction & Database Pipeline:** Fetches AU meetings, generates race cards, runs barrier/weight trifecta prediction algorithms, updates `trifecta.db`, and syncs with Google Docs/Drive.
3. **Packaging & Distribution:** Bundles daily Markdown and PDF booklets into subscriber zips and automates subscriber delivery / Stripe & Gumroad webhook sync.

**Tech Stack:** Python 3, Typer, Httpx, ReportLab, SQLite, Bash, cron / background scheduler.

**Spec:** Fair Dinkum Press & FormFav Racing Intelligence Architecture.

## Global Constraints
- **API Security:** `FORMFAV_API_KEY` must be securely loaded from `.env` or user home environment without leaking.
- **Robustness:** Network or rendering errors (e.g. ReportLab or Google Docs API hiccups) must be handled gracefully with fallbacks so the core data and prediction pipeline never fails.
- **Automation:** Zero manual intervention required for daily runs.

## Review Focus
1. **API Rate Limiting & Timeouts:** Ensuring `httpx` client handles timeouts and retries cleanly.
2. **Missing Market Odds / Staging:** Fallback behavior when pre-race market odds are not pasted (relies on barrier & weight heuristics).
3. **Subscriber Packaging:** Ensuring daily `.zip` outputs are cleanly generated and organized by date under `outputs/formfav/<DATE>/`.

---

## Tasks

### Task 1: Robust Cron & Automation Wrapper
**Files:**
- Create: `scripts/racing/run_subscription_automation.py`
- Modify: `workflow_manager/daily_formfav_fetch.sh`

**Interfaces:**
- Consumes: `workflow_manager/daily_formfav_fetch.sh`, `scripts/racing/formfav.py`
- Produces: Automated execution wrapper with health logging and error notification.

- [ ] **Step 1: Write verification script for automation wrapper**
- [ ] **Step 2: Implement cron installation helper & health check in `scripts/racing/run_subscription_automation.py`**
- [ ] **Step 3: Run test verification**
- [ ] **Step 4: Commit**

### Task 2: Subscriber Email / Delivery Dispatcher
**Files:**
- Create: `scripts/racing/dispatch_subscriber_intelligence.py`

**Interfaces:**
- Consumes: `outputs/formfav/<DATE>/*.pdf`, `outputs/formfav/<DATE>/TRIFECTA_<DATE>.md`
- Produces: Automated dispatch of daily racing intelligence packets to subscribers.

- [ ] **Step 1: Write subscriber dispatch script**
- [ ] **Step 2: Verify dispatch logic with dry-run**
- [ ] **Step 3: Commit**

---
