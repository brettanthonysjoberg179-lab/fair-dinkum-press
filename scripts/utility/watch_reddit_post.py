import subprocess
import json
import time
import os

POST_ID = "1wwobd2"
LOG_FILE = "/home/brettanthonysjoberg179/logs/reddit_watch.log"

def check_post():
    # Pass subreddit as required by schema
    payload = {"subreddit": "Entrepreneur", "max_results": 20}
    cmd = ["composio", "execute", "REDDIT_RETRIEVE_REDDIT_POST", "-d", json.dumps(payload)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout

print(f"Updating and checking post {POST_ID}...")
output = check_post()
print(output[:500])
