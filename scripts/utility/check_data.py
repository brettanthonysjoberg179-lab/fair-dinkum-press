import json

def check_data(path):
    print(f"Checking {path}")
    with open(path, "r") as f:
        res = json.load(f)
    data = res.get("data", {})
    print("data type:", type(data))
    if isinstance(data, dict):
        print("data keys:", list(data.keys()))
        print("data sample:", str(data)[:500])
    elif isinstance(data, list):
        print("data list len:", len(data))
        if data:
            print("first item sample:", str(data[0])[:500])

check_data("/tmp/composio/adhoc_aab597c00a85/GMAIL_FETCH_EMAILS_OUTPUT_29d84bae.json")
check_data("/tmp/composio/adhoc_7a6c2fb65a93/GOOGLEDRIVE_FIND_FILE_OUTPUT_d062b086.json")
