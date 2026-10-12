import json

def parse_gmail():
    path = "/tmp/composio/adhoc_aab597c00a85/GMAIL_FETCH_EMAILS_OUTPUT_29d84bae.json"
    with open(path, "r") as f:
        res = json.load(f)
    messages = res.get("data", {}).get("messages", [])
    print(f"=== GMAIL MESSAGES ({len(messages)}) ===")
    for m in messages:
        print(f"- ID: {m.get('messageId')} | Labels: {m.get('labelIds')} | Text preview: {m.get('messageText', '')[:200]}...")

def parse_drive():
    path = "/tmp/composio/adhoc_7a6c2fb65a93/GOOGLEDRIVE_FIND_FILE_OUTPUT_d062b086.json"
    with open(path, "r") as f:
        res = json.load(f)
    files = res.get("data", {}).get("files", [])
    print(f"\n=== GOOGLE DRIVE FILES ({len(files)}) ===")
    for f in files:
        print(f"- Name: {f.get('name')} | Type: {f.get('mimeType')} | ID: {f.get('id')}")

if __name__ == "__main__":
    parse_gmail()
    parse_drive()
