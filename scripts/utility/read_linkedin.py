import json
import base64

output_path = "/tmp/composio/adhoc_6818c7419e36/GMAIL_FETCH_EMAILS_OUTPUT_a0e461a5.json"

def get_body(payload):
    body = ""
    if "body" in payload and "data" in payload["body"]:
        try:
            body = base64.urlsafe_b64decode(payload["body"]["data"] + "==").decode("utf-8", errors="ignore")
        except:
            pass
    if not body and "parts" in payload:
        for part in payload["parts"]:
            body += get_body(part)
    return body

with open(output_path, "r") as f:
    data = json.load(f)

messages = data.get("response", data).get("messages", data.get("data", {}).get("messages", data))

for i, msg in enumerate(messages, 1):
    payload = msg.get("payload", {})
    headers = payload.get("headers", [])
    sender = ""
    subject = ""
    for h in headers:
        if h.get("name", "").lower() == "from":
            sender = h.get("value", "")
        if h.get("name", "").lower() == "subject":
            subject = h.get("value", "")
            
    if "linkedin" in sender.lower() or "linkedin" in subject.lower():
        print(f"\n==============================")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Snippet: {msg.get('snippet', '')}")
        body = get_body(payload)
        if body:
            print("\nBody Preview:")
            print(body[:1500])
        print(f"==============================")
