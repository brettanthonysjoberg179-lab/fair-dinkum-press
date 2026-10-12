import sys
sys.path.insert(0, '/home/brettanthonysjoberg179/rags_memory_db')
from rags_memory_db import RAGSMemoryDB

db = RAGSMemoryDB('/home/brettanthonysjoberg179/rags_memory_db/rags_memory.db')

# Store fact about Book 1 & Book 2 enterprise publishing launch
memory_content = (
    "Fair Dinkum Publishing Agent Workflowz Enterprise Fleet Update (October 2026): "
    "1. Published Book 1: 'The Autonomous Solopreneur: Building & Scaling Multi-Agent AI Enterprises' (10 chapters, EPUB, cover art, sales copy, GitHub repos: autonomous-solopreneur and opal-vista-wombat-agent). "
    "2. Published Book 2: 'Programmatic Dominance: Scaling Automated SEO & High-Velocity Content Networks' (Outline, Part I, EPUB, cover art, GitHub repo: programmatic-dominance). "
    "3. Synced product inventory to Airtable (Base: appqqwluJEP7553HY, Table: tblYavj3sIPsQeJcS) with live SKUs and priced at A$47.00. "
    "4. Emailed complimentary copies to Sally Bloomfield (sallybloomfield048@gmail.com). "
    "5. Published architecture breakdown post to r/Entrepreneur. "
    "6. Created custom skills: autonomous-solopreneur-orchestrator and gmail-recent-checker."
)

mem_id, mem_uuid = db.store(memory_content, memory_type='fact', confidence=0.95)
print(f"[+] Successfully stored memory in RAGS DB: ID {mem_id}, UUID {mem_uuid}")

print("\n--- Current RAGS Stats ---")
print(db.stats())
db.close()
