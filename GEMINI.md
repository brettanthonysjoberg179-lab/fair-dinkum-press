# Fair Dinkum Press & Autonomous Solopreneur Workspace — Project Instructions

Welcome to the central command workspace for **Fair Dinkum Press**, **AgentKit**, **FormFav Racing Intelligence**, and autonomous solopreneur AI agent systems.

## 🚀 Core Workspace Pillars & Objectives

1. **Online Business Creation**: Rapidly scaffold, test, and launch autonomous solopreneur ventures, micro-SaaS workflows, and digital agency tools.
2. **Digital Asset Monetization**: Package codebases, ebooks, workbooks, racing intelligence feeds, and automated workflows into Stripe & Gumroad digital products, subscription tiers, and bundles.
3. **Australian AI Compliance**: Ensure all AI-generated content, outreach agents, and automated data pipelines strictly adhere to Australian Privacy Principles (APPs), copyright rules, and AI regulatory frameworks (`au-ai-compliance-agent`).
4. **Autonomous Workforce & Maximum Automation**: **Maximize automation in every interaction.** Whenever a task, content pipeline, audit, or publishing workflow is requested, Gemini must autonomously design, generate, and orchestrate multi-agent workforce scripts (using Python, Composio, MCP servers, and background workers) to execute tasks end-to-end without manual intervention. Emphasize headless execution, robust logging, automated scheduling, and self-healing error recovery across all agentic teams.

## 📁 Workspace Architecture & Directory Conventions

To keep this workspace clean and maintainable, all loose files are organized functionally:

- **`/scripts/`**: Automation logic and standalone python/js workers.
  - `scripts/agentkit/`: Small Business Automation Pack scripts.
  - `scripts/racing/`: FormFav gallops scraping, form analysis, and trifecta prediction scripts.
  - `scripts/seo/`: Ahrefs API integration, programmatic SEO generators.
  - `scripts/publishing/`: Book generation, cover creation, and distribution scripts.
  - `scripts/utility/`: General utility tools (PDF generators, push scripts, uploaders).
- **`/docs/`**: Reference materials, documentation, and reports.
  - `docs/manuscripts/`: Ebook and workbook markdown manuscripts.
  - `docs/reports/`: Ahrefs SEO reports, race results, and accuracy metrics.
  - `docs/business/`: Master business profiles, operational manuals, and audits.
  - `docs/compliance/`: Australian AI compliance frameworks, Privacy Act compliance, and playbooks.
- **`/assets/`**: Static media assets (PDFs, EPUBs, generated PNG cover images/thumbnails).
- **`/web/`**: Landing pages, HTML dashboards, and front-end mockups.
- **`/data/`**: JSON configuration caches, schemas, and exported archives (`.tar.gz`).
- **Root Reserved Files**: `.env`, `wrangler.toml`, `cloudflare.env`, `.gitignore`, `_routes.json`, `FILETREE.md`.

---

## ⚙️ Engineering Standards & Workflows

1. **Execution Context**: When executing automation scripts that rely on relative directories (such as `logs/` or `outputs/`), always run them from the repository root:
   ```bash
   python scripts/agentkit/agentkit_lead_triage.py --dry-run
   ```
2. **Environment & Secrets**: 
   - Never commit `.env` or `cloudflare.env` files.
   - Use Composio and Stripe API keys securely via environment variables.
3. **Publishing & Monetization Discipline**:
   - Follow the established Fair Dinkum publishing workflow (Research → Manuscript → Cover → EPUB/PDF compilation → Gumroad/Stripe Packaging).
   - Verify every commercial release against Australian AI compliance standards and Privacy Act requirements before deployment.
4. **Git Discipline**:
   - Do not stage or commit changes unless explicitly instructed.
   - Maintain clear, concise commit messages focusing on the "why".
