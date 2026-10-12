import requests
import json
import base64

username = "brettanthonysjoberg179@gmail.com"
api_key = "0B654A13-A405-9471-77F3-D78991C14B1F"
to_number = "+17786528414"
message_body = "Fair Dinkum Publishing: Autonomous Aussie digital publisher & B2B AI compliance agency (Privacy Act APP 1.7). Stack: Python, Cloudflare Workers/R2/D1, Composio agents, programmatic SEO. Products: FOUND ON AI ($97), AU AI Compliance Playbook ($149), Empire Super-Bundle ($297), DFY Audits ($1,500)."

auth_str = f"{username}:{api_key}"
encoded_auth = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/json"
}

print("Sending SMS to US/Canada number via ClickSend API...")
send_payload = {
    "messages": [
        {
            "to": to_number,
            "body": message_body
        }
    ]
}

send_resp = requests.post("https://rest.clicksend.com/v3/sms/send", headers=headers, json=send_payload)
print(f"Send Response Status: {send_resp.status_code}")
print(send_resp.text)
