#!/usr/bin/env python3
"""
Automated Customer Feedback RAG Loop Agent
Polls customer support emails and ingests inquiries into RAGS memory for future product updates.
"""

import os
import sys
import json
import subprocess

sys.path.insert(0, '/home/brettanthonysjoberg179/rags_memory_db')
from rags_memory_db import RAGSMemoryDB

def load_env_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env_file(".env")
load_env_file("fair_dinkum_publishing/.env")

print("Initializing Customer Feedback RAG Loop Agent...")

def poll_and_ingest():
    cmd = ["composio", "execute", "GMAIL_FETCH_EMAILS", "-d", json.dumps({"query": "subject:question OR subject:help OR subject:support", "user_id": "me", "max_results": 5})]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Gmail fetch error: {res.stderr}")
        return
    
    try:
        data = json.loads(res.stdout)
        messages = data.get("response", data).get("messages", data.get("data", {}).get("messages", []))
        if not messages:
            print("[+] No pending customer support queries found.")
            return
        
        db = RAGSMemoryDB('/home/brettanthonysjoberg179/rags_memory_db/rags_memory.db')
        for msg in messages:
            snippet = msg.get("snippet", "Customer inquiry")
            content = f"Customer Support Inquiry Ingested: {snippet}"
            mem_id, mem_uuid = db.store(content, memory_type='semantic', confidence=0.88)
            print(f"[+] Ingested customer feedback into RAGS memory: ID {mem_id}")
        db.close()
    except Exception as e:
        print(f"[!] Error processing feedback loop: {e}")

if __name__ == "__main__":
    poll_and_ingest()
