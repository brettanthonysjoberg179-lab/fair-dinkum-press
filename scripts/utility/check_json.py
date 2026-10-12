import json

def check_keys(path):
    print(f"Checking {path}")
    with open(path, "r") as f:
        data = json.load(f)
    print("Top-level keys:", list(data.keys()))
    if "response_data" in data:
        print("response_data keys:", list(data["response_data"].keys()) if isinstance(data["response_data"], dict) else type(data["response_data"]))
        if isinstance(data["response_data"], dict):
            print("response_data content sample:", str(data["response_data"])[:300])

check_keys("/tmp/composio/adhoc_aab597c00a85/GMAIL_FETCH_EMAILS_OUTPUT_29d84bae.json")
check_keys("/tmp/composio/adhoc_7a6c2fb65a93/GOOGLEDRIVE_FIND_FILE_OUTPUT_d062b086.json")
