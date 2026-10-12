import json

def summarize_gmail():
    path = "/tmp/composio/adhoc_aab597c00a85/GMAIL_FETCH_EMAILS_OUTPUT_29d84bae.json"
    with open(path, "r") as f:
        data = json.load(f)
    print("=== GMAIL SUMMARY ===")
    messages = data.get("response_data", {}).get("messages", [])
    if not messages:
        messages = data.get("response_data", {}).get("data", {}).get("messages", [])
    print(f"Total messages found: {len(messages)}")
    for i, m in enumerate(messages[:15]):
        snippet = m.get("snippet", "")
        subject = ""
        sender = ""
        headers = m.get("payload", {}).get("headers", [])
        for h in headers:
            if h.get("name") == "Subject":
                subject = h.get("value")
            elif h.get("name") == "From":
                sender = h.get("value")
        print(f"{i+1}. From: {sender} | Subject: {subject} | Snippet: {snippet[:100]}")

def summarize_drive():
    path = "/tmp/composio/adhoc_7a6c2fb65a93/GOOGLEDRIVE_FIND_FILE_OUTPUT_d062b086.json"
    with open(path, "r") as f:
        data = json.load(f)
    print("\n=== GOOGLE DRIVE SUMMARY ===")
    files = data.get("response_data", {}).get("files", [])
    if not files:
        files = data.get("response_data", {}).get("data", {}).get("files", [])
    print(f"Total files found: {len(files)}")
    for i, f in enumerate(files[:30]):
        name = f.get("name", "")
        mime = f.get("mimeType", "")
        print(f"{i+1}. Name: {name} ({mime})")

if __name__ == "__main__":
    summarize_gmail()
    summarize_drive()
