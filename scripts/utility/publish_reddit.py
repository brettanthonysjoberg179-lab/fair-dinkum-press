import subprocess
import json

title = "How I stopped being a manual 'prompt jockey' and built a 24/7 multi-agent publishing enterprise (Complete Architecture Breakdown)"
text = """For the past two years, I fell into what I call the Chatbot Trap. I was opening browser tabs, typing ad-hoc prompts, and manually stitching together outputs. Even with state-of-the-art models, my human attention remained the ultimate operational bottleneck.

Last month, I decided to fix this. I shifted my role from a manual doer to the Chief Architect of an autonomous multi-agent AI workforce. 

Today, I’m open-sourcing and publishing the complete operational blueprint behind this transition in my new masterclass: "The Autonomous Solopreneur: Building & Scaling Multi-Agent AI Enterprises."

Here is the exact architecture we built and deployed:

1. Role-Specialized Agent Swarms:
- The Researcher: Gathers market data and long-tail keyword matrices.
- The Writer/Editor: Synthesizes structured markdown manuscripts with strict stylistic constraints.
- The Compliance Auditor: Scans every asset against regulatory checklists and negative constraints.
- The Publisher: Packages assets and interfaces with headless storefront APIs.

2. Tiered Memory & Vector RAG:
- Global Memory (GEMINI.md) for cross-project preferences.
- Team-Shared Instructions committed to version control.
- Private Project Memory (MEMORY.md) for local operational state.
- Vector DB Retrieval for institutional recall across past research.

3. Automated Pipelines & Headless Monetization:
- Programmatic SEO (pSEO): Generating structured content matrices at scale.
- Self-Healing QA Loops: Catching formatting errors automatically before human review.
- Headless Storefronts: Packaging validated EPUBs and cover art into ZIP bundles and syncing inventory to Airtable and Gumroad.

We’ve packaged the 10-chapter EPUB, cover art, automated email drip sequences, and companion workbook into a complete digital product kit (Live on Gumroad & synced to Airtable via Fair Dinkum Publishing Agent Workflowz).

Are you still using chat interfaces for business operations, or have you started orchestrating autonomous agent swarms? Happy to answer any questions about the technical architecture below!"""

payload = {
    "subreddit": "Entrepreneur",
    "title": title,
    "text": text,
    "kind": "self",
    "flair_id": "c2f22a12-e1d8-11e3-a77b-12313b0a74a7"  # Tools and Technology
}

cmd = ["composio", "execute", "REDDIT_CREATE_REDDIT_POST", "-d", json.dumps(payload)]
print("Publishing to r/Entrepreneur via Composio with flair...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
