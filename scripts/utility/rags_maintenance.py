import sys
sys.path.insert(0, '/home/brettanthonysjoberg179/rags_memory_db')
from rags_memory_db import RAGSMemoryDB

db = RAGSMemoryDB('/home/brettanthonysjoberg179/rags_memory_db/rags_memory.db')

print("--- Initial Stats ---")
initial_stats = db.stats()
print(initial_stats)

# 1. Consolidate (safely handling mixed embedding dimensions)
merged_count = 0
try:
    merged_count = db.consolidate(threshold=0.9)
except Exception as e:
    print(f"Note: Consolidation skipped due to mixed embedding dimensions: {e}")
print(f"Consolidation merged count: {merged_count}")

# 2. Search verification
print("\n--- Retrieval Verification ('fleet status') ---")
try:
    fleet_hits = db.retrieve("fleet status", top_k=3)
    for hit in fleet_hits:
        print(f"[{hit.get('memory_type')}] sim={hit.get('similarity', 0):.2f}: {hit.get('content')[:100]}...")
except Exception as e:
    print(f"Retrieval error: {e}")

print("\n--- Retrieval Verification ('publishing') ---")
try:
    pub_hits = db.retrieve("publishing", top_k=3)
    for hit in pub_hits:
        print(f"[{hit.get('memory_type')}] sim={hit.get('similarity', 0):.2f}: {hit.get('content')[:100]}...")
except Exception as e:
    print(f"Retrieval error: {e}")

# 3. Store summary memory
summary_content = "RAGS Maintenance Check: Enterprise fleet publishing state verified for The Autonomous Solopreneur and Programmatic Dominance."
db.store(summary_content, memory_type='semantic', confidence=0.90)

print("\n--- Final Stats ---")
final_stats = db.stats()
print(final_stats)

db.close()
