import sys
sys.path.insert(0, '/home/brettanthonysjoberg179/rags_memory_db')
from rags_memory_db import RAGSMemoryDB

db = RAGSMemoryDB('/home/brettanthonysjoberg179/rags_memory_db/rags_memory.db')

feedback_content = (
    "Community Feedback Loop (r/Entrepreneur post 1wwobd2): "
    "Readers are highly interested in concrete examples of tiered memory implementation (GEMINI.md structure) "
    "and how compliance agents handle false positives. Action: Expand Chapter 3 and Chapter 5 in the next revision "
    "with code-level examples of tiered memory routing and compliance rule exceptions."
)

mem_id, mem_uuid = db.store(feedback_content, memory_type='semantic', confidence=0.92)
print(f"[+] Stored community feedback loop in RAGS DB: ID {mem_id}")
db.close()
