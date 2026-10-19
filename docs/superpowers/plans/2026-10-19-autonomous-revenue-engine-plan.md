# 100% Automated Revenue Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 100% automated, zero-touch revenue engine across 4 modular components: Automated Data Ingestion, Automated Packaging & Publishing, Programmatic SEO Acquisition, and Zero-Touch Webhook Delivery.

**Architecture:** A modular Python backend using scheduled cron/background workers, FormFav API / web scraping for data ingestion, Markdown-to-PDF/EPUB synthesis, programmatic landing page generation, and secure Stripe/Gumroad webhook verification.

**Tech Stack:** Python 3.11+, PyYAML, Requests, Jinja2, ReportLab/WeasyPrint (or markdown/pdfkit), FastAPI/Flask for webhook handling, SQLite/JSON state management.

**Spec:** Autonomous Solopreneur Revenue Engine (Fair Dinkum Press / FormFav / AgentKit)

## Global Constraints

- **Execution Root:** Run all scripts from repository root (`/home/brettanthonysjoberg179`).
- **No Secrets in Repo:** Environment variables (`STRIPE_API_KEY`, `GUMROAD_ACCESS_TOKEN`, `FORMFAV_API_KEY`) must be loaded from `.env` or `.env.local`.
- **Idempotency & Error Recovery:** Every script must log to `logs/` and handle network/API failures gracefully without crashing the scheduler.

## Review Focus

1. **API Rate Limits / Failures:** What happens if FormFav or external APIs return 429/500? (Handled with exponential backoff and fallback cached data).
2. **Invalid Webhook Signatures:** Unauthorized requests to webhook endpoints must return 400 Bad Request immediately.
3. **File System Permission / Missing Directories:** Ensure `outputs/`, `data/`, and `logs/` directories are auto-created on startup.
4. **Duplicate Content Generation:** Programmatic SEO and publishing tasks must check existing output records to prevent duplicate publications.

---

### Task 1: Automated Data Ingestion & Synthesis Engine

**Files:**
- Create: `scripts/racing/autonomous_ingestion.py`
- Test: `tests/test_autonomous_ingestion.py`

**Interfaces:**
- Consumes: Environment variables (`FORMFAV_API_KEY`), network access.
- Produces: `data/racing_digest_latest.json` and synthesized Markdown digest in `docs/reports/`.

- [ ] **Step 1: Write failing test for data ingestion & digest generation**

```python
import os
import json
from pathlib import Path
import pytest

def test_ingestion_creates_output(tmp_path):
    from scripts.racing.autonomous_ingestion import ingest_and_synthesize
    output_json = tmp_path / "racing_digest.json"
    result = ingest_and_synthesize(output_path=output_json, dry_run=True)
    assert result is True
    assert output_json.exists()
    data = json.loads(output_json.read_text())
    assert "meetings" in data
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_autonomous_ingestion.py -v`
Expected: FAIL with `ModuleNotFoundError` or test failure.

- [ ] **Step 3: Implement `autonomous_ingestion.py`**

Create `scripts/racing/autonomous_ingestion.py` implementing automated fetching, fallback mock data for dry-run/testing, and JSON/Markdown synthesis.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_autonomous_ingestion.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/racing/autonomous_ingestion.py tests/test_autonomous_ingestion.py
git commit -m "feat(racing): add autonomous data ingestion and synthesis engine"
```

---

### Task 2: Automated Packaging & Publishing (`storefront-publisher`)

**Files:**
- Create: `scripts/publishing/autonomous_publisher.py`
- Test: `tests/test_autonomous_publisher.py`

**Interfaces:**
- Consumes: `data/racing_digest_latest.json` or Markdown reports.
- Produces: Formatted PDF/EPUB booklet in `assets/` and simulated Gumroad/Stripe product SKU registration.

- [ ] **Step 1: Write failing test for packaging and publishing**

```python
import pytest
from pathlib import Path

def test_publisher_packaging(tmp_path):
    from scripts.publishing.autonomous_publisher import package_digital_product
    report_file = tmp_path / "sample_report.md"
    report_file.write_text("# Test Racing Intelligence Report\nData content...")
    
    output_pdf = tmp_path / "output.pdf"
    res = package_digital_product(source_md=report_file, output_pdf=output_pdf, dry_run=True)
    assert res is True
    assert output_pdf.exists()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_autonomous_publisher.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `autonomous_publisher.py`**

Create `scripts/publishing/autonomous_publisher.py` to handle PDF/EPUB compilation and storefront SKU synchronization.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_autonomous_publisher.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/publishing/autonomous_publisher.py tests/test_autonomous_publisher.py
git commit -m "feat(publishing): add automated digital product packaging and publishing"
```

---

### Task 3: Autonomous Programmatic SEO Traffic Acquisition

**Files:**
- Create: `scripts/seo/programmatic_seo_generator.py`
- Test: `tests/test_programmatic_seo.py`

**Interfaces:**
- Consumes: Keyword matrix JSON / configuration.
- Produces: Generated landing pages in `web/` or `programmatic_seo_outputs/`.

- [ ] **Step 1: Write failing test for programmatic SEO landing page generation**

```python
import pytest
from pathlib import Path

def test_pseo_generation(tmp_path):
    from scripts.seo.programmatic_seo_generator import generate_landing_pages
    output_dir = tmp_path / "pages"
    count = generate_landing_pages(output_dir=output_dir, dry_run=True)
    assert count > 0
    assert (output_dir / "index.html").exists() or len(list(output_dir.glob("*.html"))) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_programmatic_seo.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `programmatic_seo_generator.py`**

Create `scripts/seo/programmatic_seo_generator.py` to batch-generate high-intent landing pages from data templates.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_programmatic_seo.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/seo/programmatic_seo_generator.py tests/test_programmatic_seo.py
git commit -m "feat(seo): add programmatic SEO landing page generator"
```

---

### Task 4: Zero-Touch Revenue Webhook & Delivery Server

**Files:**
- Create: `scripts/utility/revenue_webhook_server.py`
- Test: `tests/test_revenue_webhook.py`

**Interfaces:**
- Consumes: Incoming HTTP POST requests from Stripe / Gumroad webhooks.
- Produces: Automated fulfillment email/download link dispatch and ledger logging.

- [ ] **Step 1: Write failing test for webhook verification and fulfillment**

```python
import pytest
from fastapi.testclient import TestClient

def test_webhook_fulfillment():
    from scripts.utility.revenue_webhook_server import app
    client = TestClient(app)
    response = client.post("/webhook/stripe", json={"type": "checkout.session.completed", "data": {"object": {"customer_email": "test@example.com"}}})
    assert response.status_code in [200, 400] # depending on signature header check
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_revenue_webhook.py -v`
Expected: FAIL

- [ ] **Step 3: Implement `revenue_webhook_server.py`**

Create `scripts/utility/revenue_webhook_server.py` using FastAPI to securely process payments and trigger instant digital delivery.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_revenue_webhook.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/utility/revenue_webhook_server.py tests/test_revenue_webhook.py
git commit -m "feat(webhooks): add zero-touch revenue webhook fulfillment server"
```
