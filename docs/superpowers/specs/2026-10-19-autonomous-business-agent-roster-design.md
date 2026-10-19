# Autonomous Enterprise Engine Design Specification

## 1. Executive Summary & Intent
This specification defines the architecture for a 99% autonomous annual business engine operating from **June 1 through May 31** each year. The system integrates three core operational pillars—**Automated Digital Publishing & Content Syndication**, **Client Lead Triage & Sales Outreach**, and **Software Micro-SaaS Operations**—orchestrated 24/7 by specialized AI agents on a rotating roster. 

Crucially, the system features a **Gmail-based Human-In-The-Loop (HITL) Communication Bus**, allowing the user to manage, query, and approve high-stakes agent actions simply by emailing dedicated agent addresses or replying to automated digest and approval threads.

---

## 2. Core Pillars & Agent Roster

### Pillar A: Automated Digital Publishing & Content Syndication
- **Agents**: Keyword Research Agent, Content Writer Agent, Nano Banana Image Agent, SEO Optimizer Agent, Publisher Agent.
- **Workflow**: 
  1. Discovers high-potential keywords and GSC striking-distance topics.
  2. Drafts SEO-optimized blog posts, ebooks, and landing pages.
  3. Generates custom cover images and visual assets.
  4. Publishes to WordPress, headless CMS, and storefronts (Gumroad/Stripe) with automated markdown formatting and schema markup.

### Pillar B: Client Lead Triage & Sales Outreach
- **Agents**: Inbound Monitor Agent, Lead Scoring Agent, Outreach Copywriter Agent, CRM Sync Agent (GoHighLevel/Composio).
- **Workflow**:
  1. Monitors inbox, form submissions, and social DMs 24/7.
  2. Qualifies leads against ICP (Ideal Customer Profile) criteria.
  3. Triggers personalized outreach sequences or assigns high-intent leads to the user's priority queue.
  4. Automatically syncs pipeline stages in GoHighLevel / CRM.

### Pillar C: Software Micro-SaaS Operations
- **Agents**: Uptime Watcher Agent, Stripe Billing Agent, Self-Healing Bugfix Agent, Metrics Aggregator Agent.
- **Workflow**:
  1. Continuously health-checks micro-SaaS endpoints and Cloudflare Workers.
  2. Processes Stripe webhook events (subscriptions, renewals, failed payments).
  3. Logs errors, runs diagnostics, and drafts hotfix PRs for review.
  4. Aggregates daily financial and operational metrics.

---

## 3. Technical Architecture & Tech Stack

- **Language & Runtime**: Python 3.11+, `asyncio`, FastAPI for webhook endpoints.
- **Scheduler**: APScheduler / Async background workers running 24/7.
- **State & Memory**: SQLite database (`data/autonomous_business.db`) + RAGS Vector Memory DB (`rags_memory_db`) for long-term agent context.
- **Communication Bus (Gmail HITL)**: 
  - Uses Gmail API (via Composio / Google API OAuth integration).
  - Dedicated agent aliases or thread-tagged routing (e.g., `publishing@domain`, `leads@domain`, `saas@domain`, `commander@domain`).
  - Polling interval: Every 60 seconds, the Gmail Gateway fetches unread emails, parses sender intent, validates authorization, and queues agent commands.

---

## 4. Annual Calendar & 24/7 Schedule

- **Annual Kickoff (June 1)**: Automatic system reset, revenue targets calibration, new annual content calendar generated from Search Console data, budget allocations locked.
- **Daily Roster**:
  - **06:00 UTC**: Executive Morning Digest sent to user's primary inbox summarizing previous 24h metrics (revenue, leads, published posts, system health).
  - **Every 30m**: Lead Triage & Sales Outreach execution loop.
  - **Every 2h**: Content Publishing & Syndication execution loop.
  - **Continuous (Every 5m)**: SaaS Infrastructure & Webhook processing loop.
- **Weekly Roster (Sundays)**: SEO drift analysis, backlink audit, financial reconciliation.

---

## 5. Gmail HITL Workflow Specification

1. **Approval Request**: When an agent encounters a high-risk action (e.g., publishing a paid campaign, refunding >$50, or deploying code changes), it pauses execution and dispatches an email to the user:
   - *Subject*: `[ACTION REQUIRED] Publishing Agent: Approve Article #42 "Autonomous AI Workflows"`
   - *Body*: Details of the proposed action, risk score, and preview links.
   - *Reply Options*: User replies `APPROVED` or `REJECTED: <reason>`.
2. **Direct Chat**: User can email `commander@domain` or any agent alias with plain-text instructions (e.g., "Shift focus to B2B lead generation this week" or "Draft a post about Cloudflare Workers"). The agent parses the instruction, updates its state, and confirms via email.
