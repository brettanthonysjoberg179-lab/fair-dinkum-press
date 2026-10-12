import requests
import json
import base64

username = "brettanthonysjoberg179@gmail.com"
api_key = "0B654A13-A405-9471-77F3-D78991C14B1F"
message_id = "1F1C3CC6-1B85-6508-BB7B-A9FB57F9A6AB"

auth_str = f"{username}:{api_key}"
encoded_auth = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/json"
}

print("Fetching SMS history...")
hist_resp = requests.get("https://rest.clicksend.com/v3/sms/history", headers=headers)
print(hist_resp.status_code)
print(hist_resp.text)

print("\nFetching SMS receipts...")
receipts_resp = requests.get("https://rest.clicksend.com/v3/sms/receipts", headers=headers)
print(receipts_resp.status_code)
print(receipts_resp.text)
