# Solopreneur Command Center Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a fully functional Solopreneur Command Center Dashboard web app and website featuring live agent task monitoring, product inventory, sales/revenue metrics, Ahrefs SEO keywords, traffic statistics, and blog/publishing feed.

**Architecture:** Python FastAPI backend service (`scripts/dashboard/server.py`) that aggregates data from workspace inventory JSONs, SQLite databases, and output logs, serving a modern Vanilla CSS / HTML single-page dashboard (`web/command-center/index.html`) with real-time JSON polling and interactive widgets.

**Tech Stack:** Python (FastAPI, uvicorn), Vanilla CSS (Glassmorphism dark theme), HTML5, JavaScript (Fetch API, dynamic rendering).

**Spec:** `docs/superpowers/specs/2026-10-16-solopreneur-command-center-design.md`

## Global Constraints
- **Styling**: Vanilla CSS only (no Tailwind CSS).
- **Architecture**: Modular separation between data aggregator API (`server.py`) and frontend UI (`index.html`).
- **Data Source**: Live aggregation from workspace `data/`, `outputs/`, and catalogs.

## Review Focus
1. **API Error Resilience**: Graceful fallback when optional database or report files are missing.
2. **Responsive Layout**: Clean grid scaling across desktop and mobile screens.
3. **Real-Time Data Polling**: Auto-refreshing KPIs and agent task status.

---

## Tasks

### Task 1: Data Aggregator API Backend

**Files:**
- Create: `scripts/dashboard/server.py`
- Test: `tests/test_dashboard_server.py`

**Interfaces:**
- Consumes: Workspace JSON catalogs (`gumroad-storefront/catalog.json`, `ahrefs_report_fairdinkum.press_2026-10-14.md`, agent logs)
- Produces: REST API endpoints `/api/metrics`, `/api/agents`, `/api/products`, `/api/seo`, `/api/blog`

- [ ] **Step 1: Write the test for API endpoints**
- [ ] **Step 2: Implement FastAPI server aggregating workspace data**
- [ ] **Step 3: Verify server starts and returns JSON metrics**
- [ ] **Step 4: Commit**

### Task 2: Command Center Frontend UI

**Files:**
- Create: `web/command-center/index.html`
- Create: `web/command-center/styles.css`
- Create: `web/command-center/app.js`

**Interfaces:**
- Consumes: `/api/*` endpoints from FastAPI backend
- Produces: Interactive executive dashboard with widgets for KPIs, agent tasks, products, SEO, traffic, and blog.

- [ ] **Step 1: Create HTML structure with glassmorphism CSS styling**
- [ ] **Step 2: Implement JavaScript fetch logic and dynamic UI rendering**
- [ ] **Step 3: Test local web app launch and UI responsiveness**
- [ ] **Step 4: Commit**
