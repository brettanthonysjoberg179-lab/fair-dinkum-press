import sys
sys.path.insert(0, '/home/brettanthonysjoberg179/rags_memory_db')
try:
    from rags_memory_db import RAGSMemoryDB
    db = RAGSMemoryDB('/home/brettanthonysjoberg179/rags_memory_db/rags_memory.db')
    
    memory_content = (
        "Fair Dinkum Publishing Business Plan (2026-09-25) Execution Record: "
        "1. Document ID: 10h3SBJz7zUfHFZTLd6n_OdDb60d86GCRKMuarXR_d5U (https://docs.google.com/document/d/10h3SBJz7zUfHFZTLd6n_OdDb60d86GCRKMuarXR_d5U/edit). "
        "2. Email Message ID: 1a111d080ef34b89 (sent to brettanthonysjoberg179@gmail.com with business-plan-2026-09-25.pdf attached). "
        "3. Financial Projections (AUD): Conservative A$1,482/yr, Base A$5,615/yr, Optimistic A$20,064/yr. "
        "4. Asset Inventory: 5 Live SKUs (A$181 basket), 14 PDFs built (US$498 value), MCP & Agent suites in pipeline."
    )
    
    mem_id, mem_uuid = db.store(memory_content, memory_type='fact', confidence=0.9)
    print(f"[+] Successfully stored Business Plan record in RAGS DB: ID {mem_id}, UUID {mem_uuid}")
    db.close()
except Exception as e:
    print(f"RAGS logging note: {e}")
