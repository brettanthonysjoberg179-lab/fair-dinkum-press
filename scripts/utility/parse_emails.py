import json

output_path = "/tmp/composio/adhoc_6818c7419e36/GMAIL_FETCH_EMAILS_OUTPUT_a0e461a5.json"
try:
    with open(output_path, "r") as f:
        data = json.load(f)
    
    messages = []
    # Check data structures
    if isinstance(data, dict):
        # Look for messages in common response paths
        resp = data.get("response", data)
        if isinstance(resp, dict):
            messages = resp.get("messages", resp.get("data", {}).get("messages", []))
        elif isinstance(resp, list):
            messages = resp
    
    if not messages and isinstance(data, list):
        messages = data

    print(f"Total messages retrieved: {len(messages)}")
    
    for i, msg in enumerate(messages[:10], 1):
        # Extract headers and snippet
        payload = msg.get("payload", {})
        headers = payload.get("headers", [])
        subject = "No Subject"
        sender = "Unknown Sender"
        date = "Unknown Date"
        
        for h in headers:
            name = h.get("name", "").lower()
            if name == "subject":
                subject = h.get("value")
            elif name == "from":
                sender = h.get("value")
            elif name == "date":
                date = h.get("value")
                
        snippet = msg.get("snippet", msg.get("bodySnippet", ""))
        print(f"\n--- Email {i} ---")
        print(f"From:    {sender}")
        print(f"Subject: {subject}")
        print(f"Date:    {date}")
        print(f"Snippet: {snippet[:120]}...")

except Exception as e:
    print(f"Error parsing email output: {e}")
    import traceback
    traceback.print_exc()
