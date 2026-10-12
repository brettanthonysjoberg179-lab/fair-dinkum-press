import requests
import json
import base64

username = "brettanthonysjoberg179@gmail.com"
api_key = "0B654A13-A405-9471-77F3-D78991C14B1F"

auth_str = f"{username}:{api_key}"
encoded_auth = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/json"
}

print("Checking user countries restrictions...")
resp = requests.get("https://rest.clicksend.com/v3/user-countries", headers=headers)
print(resp.status_code)
print(resp.text)

print("Checking SMS history / receipts...")
receipts_resp = requests.get("https://rest.clicksend.com/v3/sms/history", headers=headers)
print(receipts_resp.status_code)
print(receipts_resp.text)
