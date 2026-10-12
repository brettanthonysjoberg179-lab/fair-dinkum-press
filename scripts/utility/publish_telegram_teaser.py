import subprocess
import json

teaser = """📚 **FAIR DINKUM PUBLISHING · MASTERCLASS & BOOK LIBRARY** 🚀

Stop prompting. Start orchestrating. Here is your complete library for building, scaling, and automating a 24/7 digital enterprise with AI agent swarms:

1️⃣ **The Autonomous Solopreneur**
*Building & Scaling Multi-Agent AI Enterprises*
The definitive blueprint for shifting from manual prompt jockey to Chief Architect of role-specialized agent swarms.

2️⃣ **Programmatic Dominance**
*Scaling Automated SEO & High-Velocity Content Networks*
Master pSEO keyword matrices, automated content factories, and self-healing QA loops to capture organic search traffic at scale.

3️⃣ **MCP Orchestration Playbook**
*Run a one-person publishing empire with coordinated AI agents via Model Context Protocol.*

4️⃣ **FOUND ON AI**
*The Fair Dinkum GEO Playbook for Aussie Local Business (Rank #1 on ChatGPT, Perplexity & Gemini).*

5️⃣ **AU AI Compliance Playbook**
*Privacy Act 1988 compliance, checklists, and legal guardrails for Australian small business.*

6️⃣ **Aussie Agent Workflowz**
*The Fair Dinkum AI Side-Hustle Playbook.*

👉 Available now on Gumroad & synced via Fair Dinkum Publishing Agent Workflowz!
"""

with open("outputs/telegram_teaser.md", "w") as f:
    f.write(teaser)

print("Telegram book library teaser saved to outputs/telegram_teaser.md")
print("\nTeaser Content:\n" + teaser)
