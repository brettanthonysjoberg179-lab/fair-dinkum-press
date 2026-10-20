# Standard Operating Procedure (SOP): Autonomous Digital Publishing & Kaggle Integration
**Fair Dinkum Press & AgentKit Operations**

- **SOP Number:** FD-002
- **Version:** 2.0
- **Effective Date:** October 20, 2026
- **Review Date:** October 20, 2027
- **Author:** Autonomous Solopreneur Orchestrator / Chief Architect

---

## 1. Purpose
The purpose of this SOP is to define the operational standards, autonomous agent workflows, and publishing protocols for **Fair Dinkum Press**, integrating traditional digital publishing (eBooks, workbooks) with programmatic data publishing and AI model distribution via Kaggle.

## 2. Core Business Principles (Brian Tracy Framework)
All operations within Fair Dinkum Press adhere to foundational entrepreneurial principles:
1. **Zero-Based Thinking:** Regularly evaluate all active workflows, scripts, and products by asking: *"Knowing what I now know, would I start this today?"* If not, automate, pivot, or deprecate.
2. **Worst Possible Outcome (WPO):** Identify and accept worst-case scenarios before launching campaigns or deploying automation scripts to eliminate paralysis and ensure robust error handling.
3. **Principle of Constraints:** Relentlessly identify the primary choke point in the publishing pipeline (e.g., content generation bottlenecks, formatting errors, API rate limits) and resolve internal constraints first.
4. **The Seven Greats:** Maintain uncompromising standards in Leadership, Product Quality, Business Planning, Marketing, Sales, Economic Metrics (token ROI, conversion rates), and Customer Experience.

---

## 3. Scope & Responsibilities
- **Chief Architect (Human):** Strategic direction, final governance gates, and capital allocation.
- **Autonomous Agent Swarms (AI Workforce):** Research, content generation, regulatory compliance auditing, packaging, and multi-platform publishing.
- **Production & Publishing Team:** Oversight of markdown compilation, PDF typesetting, Kaggle dataset uploads, and storefront synchronization.

---

## 4. Standard Operating Procedures

### 4.1 Automated Content & Manuscript Production
1. **Research & Ideation:**
   - Run keyword research and market intelligence scans via Ahrefs and Search Console MCP connectors.
   - Store raw research notes in structured JSON/markdown artifacts.
2. **Drafting & Editing:**
   - Execute multi-stage generation pipelines (Researcher → Writer → Editor).
   - Ensure adherence to E-E-A-T and Helpful Content guidelines.
3. **Quality Assurance & Compliance:**
   - Pass all generated assets through the Australian AI Compliance Auditor agent (`au-ai-compliance-agent`) to verify adherence to Privacy Act regulations and APPs.

### 4.2 Kaggle Publishing Integration Pipeline
To maximize reach and monetize data assets, research datasets, and machine learning models, Fair Dinkum Press utilizes an automated Kaggle publishing workflow:
1. **Dataset Packaging (`scripts/publishing/kaggle_publisher.py`):**
   - Gather structured datasets (e.g., racing intelligence feeds, programmatic SEO matrices, financial benchmark logs) into clean CSV/JSON formats.
   - Generate metadata configuration (`dataset-metadata.json`) containing title, subtitle, description, and open licenses.
2. **Kaggle API / MCP Deployment:**
   - Utilize Kaggle API tools (`mcp_kaggle_upload_dataset_file`, `mcp_kaggle_get_dataset_status`) to push datasets to Kaggle.
   - Publish companion analysis notebooks using `mcp_kaggle_save_notebook` to demonstrate data utility and drive reader engagement.
3. **Model & Artifact Versioning:**
   - Publish fine-tuned weights or prompt-toolkit models using `mcp_kaggle_create_model` and `mcp_kaggle_update_model_variation`.

### 4.3 Headless Storefront Distribution (Gumroad & Stripe)
1. **Asset Compilation:** Assemble validated PDFs, covers, and bonus toolkits into standardized release bundles.
2. **Storefront Sync:** Publish SKUs, set pricing tiers, and configure automated webhook listeners via Gumroad and Stripe APIs.
3. **Dry-Run Discipline:** Always execute storefront deployment scripts in `--dry-run` mode first to validate API payloads and prevent configuration drift.

### 4.4 Customer Service & Feedback Loops
1. **Automated Triage:** Inbound support and customer inquiries are triaged by AI agents for instant resolution or escalated to human review queues.
2. **Iterative Refinement:** Customer feedback is ingested into the private project memory (`MEMORY.md`) to drive continuous improvement in subsequent product releases.

---

## 5. Documentation & Version Control
- All orchestration scripts, SOPs, and manuscripts are version-controlled via Git.
- Sensitive credentials (`.env`, `cloudflare.env`, API tokens) must never be committed.

## 6. Review & Revision
This SOP is reviewed quarterly by the Chief Architect and updated to reflect advancements in agentic automation and platform APIs.
