# 🇦🇺 FAIR DINKUM PUBLISHING & AI ADVISORY
## Master Business Operations Manual & Autonomous Agent Architecture

**Effective Date:** October 9, 2026  
**Status:** Operational / Production-Ready  
**Founder & Managing Director:** Brett Sjoberg  
**Jurisdiction:** Australia (Federal Privacy Act 1988, Corporations Act 2001)  

---

## 1. Executive Corporate Structure & Governance

### 1.1 Mission Statement
Fair Dinkum Publishing & AI Advisory delivers frictionless, edge-native digital publishing and B2B artificial intelligence compliance advisory. We bridge the gap between complex regulatory mandates (specifically the Australian Privacy Act 1988 and APP 1.7 Automated Decision-Making disclosures) and modern autonomous AI business operations.

### 1.2 Legal & Tax Compliance Framework
* **Entity Type:** Australian Sole Trader / Proprietary Limited (Pty Ltd) holding Australian Business Number (ABN) and Business Name registration.
* **Taxation:** Goods and Services Tax (GST) registered where turnover exceeds threshold; digital products taxed under standard Australian digital service rules.
* **Privacy & Compliance Rails (`compliance-rails/`):**
  * **APP 1.7 Compliance:** Every automated decision-making system operated by Fair Dinkum or its clients maintains transparent public disclosure registers.
  * **Data Sovereignty:** Customer data, SQLite D1 ledgers, and R2 assets are stored securely within Cloudflare's Australian/Global edge network under strict data protection protocols.

---

## 2. Product Catalog & Value Ladder

Fair Dinkum operates a high-margin, scalable digital product value ladder paired with high-ticket advisory:

| Tier | Product Name | Price (AUD) | Format / Delivery | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | *Geo-Keyword & Prompt Toolkit* | $29 – $49 | PDF / EPUB / ZIP via R2 Signed URL | Quick-start prompt engineering and local AI search visibility checklists. |
| **Tier 2** | *FOUND ON AI* | $97 | Digital Book + 5 Niche AI Agent Workflows | Playbook showing tradies, cafes, and local services how to get recommended by ChatGPT, Perplexity, and Gemini. |
| **Tier 3** | *The AU AI Compliance Playbook* | $149 | Complete Compliance Package + Templates | Essential guide for Aussie fintechs, lenders, and e-commerce to master Privacy Act APP 1.7 compliance before December 10, 2026. |
| **Tier 4** | *Autonomous Solopreneur Empire Super-Bundle* | $297 | Complete Asset Inventory, EPUBs, Workbooks, Automation Scripts | Full turnkey digital business in a box with source code, marketing copy, and sales funnels. |
| **Tier 5** | *DFY AI Compliance Audit & Advisory* | $1,500 | Custom PDF Audit Report + 1-on-1 Strategy Session | Done-For-You automated compliance scan and advisory report delivered via autonomous scanner agents. |

---

## 3. Cloudflare Edge Architecture & Infrastructure

Fair Dinkum operates a zero-maintenance, serverless edge infrastructure hosted on Cloudflare:

```
[Client / Browser] ---> [Cloudflare CDN / Pages / Workers] ---> [Cloudflare R2 Bucket (Digital Asset ZIPs)]
                                 |
                                 +---> [Cloudflare D1 SQLite (Leads & Sales Ledger)]
                                 |
                                 +---> [Cloudflare Access / Zero Trust (Admin Control Centre)]
```

* **Cloudflare Workers (`worker.js`):** Edge compute handling Stripe & Gumroad webhook events instantly at sub-50ms latency.
* **Cloudflare R2 Storage (`cloudflare_r2_uploader.py`):** Secure object storage for heavy EPUBs, ZIP packages, and book covers with zero egress fees and automated 7-day signed download URL generation.
* **Cloudflare D1 / KV (`schema.sql`):** Edge SQLite database tracking B2B regulatory prospects (e.g., Jacaranda Finance, Money3, Hume Bank) and transactional ledgers.
* **Cloudflare Access (Zero Trust):** Secures internal agent control centres behind Email OTP and GitHub OAuth.

---

## 4. Autonomous Agentic Workforce & Tooling Architecture

Fair Dinkum deploys an autonomous agentic workforce powered by **Composio**, Python, and LLM backends to execute core business functions without manual overhead.

### 4.1 Agent Roles & Responsibilities

| Agent Name | Primary Operational Domain | Connected Apps / Toolkits | Trigger / Schedule |
| :--- | :--- | :--- | :--- |
| **Outreach Growth Agent** | B2B lead generation & compliance audit pitching | Gmail, Composio Proxy, D1 SQLite | Daily cron / Event-driven |
| **Inbox Listener Agent** | Inbound customer inquiry and order processing | Gmail, Google Calendar, Composio API | Real-time Webhook (`composio listen`) |
| **SMS Review Flywheel Agent** | Post-job customer review requests & retention | ClickSend SMS (`CLICKSEND_CREATE_SMS_SEND`) | 1 hour post-job trigger |
| **Financial Ledger & Tax Agent** | Automated revenue tracking & invoicing | Airtable, Google Sheets (`upload_to_sheets.py`) | Hourly / End of Day |
| **Content Syndicator Agent** | Programmatic SEO and social posting | WordPress / Gumroad API, Reddit Bot (`publish_reddit.py`) | Weekly batch |

---

## 5. Standard Operating Procedures (SOPs)

### 5.1 SOP-001: Digital Product Packaging & Publishing
1. **Drafting:** Compile Markdown manuscript and workbook in root directory (`programmatic_dominance_manuscript.md`, etc.).
2. **Cover Generation:** Generate professional covers using `generate_book_cover.py` or image generation pipelines.
3. **Packaging:** Run `package_for_gumroad.py` to bundle EPUB, PDF, and bonuses into a clean `.zip` archive.
4. **Cloudflare R2 Upload:** Upload zip archive to R2 bucket using `cloudflare_r2_uploader.py`.
5. **Storefront Listing:** Publish SKU on Gumroad and Stripe store (`gumroad-store.html`).

### 5.2 SOP-002: B2B Compliance Outreach & Lead Generation
1. **Prospect Identification:** Run programmatic SEO generator (`programmatic_seo_generator.py`) to discover target Aussie financial and lending entities with APP 1.7 compliance gaps.
2. **Audit Generation:** Generate customized compliance audit report (`AI_COMPLIANCE_LAUNCH_PACKET.md`).
3. **Automated Outreach:** Dispatch personalized email outreach via Gmail Composio agent (`composio_outreach_agent.py`).
4. **Follow-Up & SMS:** Nudge high-value prospects via ClickSend SMS (`CLICKSEND_CREATE_SMS_SEND`) once verified.

### 5.3 SOP-003: Customer Fulfillment & Review Flywheel
1. **Webhook Capture:** Stripe/Gumroad webhook hits Cloudflare Worker (`worker.js`).
2. **Instant Delivery:** Worker generates 7-day R2 signed download URL and emails customer via transactional email.
3. **Review Request (SMS):** Schedule automated review request SMS to dispatch 1 hour after service completion:
   > *"G'day [Name], Mick here from Fair Dinkum. Stoked we sorted your project today. Mind dropping us a Google review? Keeps the local crew busy: [Short Link]"*

---

## 6. Continuous Improvement & Audit Protocol
* **Weekly Metrics Review:** Evaluate sales conversion rates, R2 download bandwidth, and email open rates via `fair-dinkum-metrics-dashboard`.
* **Compliance Review:** Update regulatory disclosures quarterly to align with changes to the Australian Privacy Act and ACCC guidelines.
