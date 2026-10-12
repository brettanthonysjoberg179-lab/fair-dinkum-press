import json, subprocess

body = """Hi,

Here is your copy of The AU AI Compliance Playbook: Small Business Guide to Privacy Act 1988 + Automated Decisions.

207 pages, covering all 10 chapters:
1. The Compliance Crisis
2. The Privacy Act
3. OAIC Enforcement
4. Mapping Your AI
5. The 90-Day Checklist
6. Privacy Policy
7. Internal AI-Use
8. Decision Tree
9. Voluntary AI Safety Standard
10. Going Live: Rollout, Audit and Ongoing Compliance

Attached as PDF. Enjoy, and if it prompts a question I can answer, just reply.

Kind regards,
Brett
Fair Dinkum Publishing
"""

PDF = "/home/brettanthonysjoberg179/play-books-upload/ready/AU_AI_Compliance_Playbook_Final.pdf"

payload = {
    "recipient_email": "lynettediehm80@gmail.com",
    "subject": "Your copy: The AU AI Compliance Playbook (Privacy Act 1988 + Automated Decisions)",
    "body": body,
    "is_html": False,
    "attachment": PDF,
}

r = subprocess.run(
    ["composio", "execute", "GMAIL_SEND_EMAIL", "-d", json.dumps(payload)],
    capture_output=True, text=True, timeout=180,
)
print("RC", r.returncode)
print(r.stdout[:2000])
print("ERR", r.stderr[:1000])
