import os
import smtplib
from email.message import EmailMessage

def load_env_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env_file(".env")
load_env_file("fair_dinkum_publishing/.env")

TO = "brettanthonysjoberg179@gmail.com"
FROM = "brettanthonysjoberg179@gmail.com"
APP_PASSWORD = "nzjawvvsggfnuryc"
SUBJECT = "Your Fair Dinkum Publishing LinkedIn Post Markdown 🚀"

# Read markdown file
md_path = "fair_dinkum_linkedin_post.md"
content = ""
if os.path.exists(md_path):
    with open(md_path, "r") as f:
        content = f.read()
else:
    content = "LinkedIn post content not found."

BODY = (
    "Hi Brett,\n\n"
    "Here is your requested Fair Dinkum Publishing LinkedIn post markdown content:\n\n"
    "--------------------------------------------------\n\n"
    f"{content}\n\n"
    "--------------------------------------------------\n\n"
    "Best regards,\n"
    "Your Autonomous Agent Workspace"
)

msg = EmailMessage()
msg["From"] = f"Brett Sjoberg <{FROM}>"
msg["To"] = TO
msg["Subject"] = SUBJECT
msg.set_content(BODY, subtype="plain", charset="utf-8")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
        s.login(FROM, APP_PASSWORD)
        s.send_message(msg)
    print(f"Successfully emailed LinkedIn post markdown to {TO}")
except Exception as exc:
    print(f"SMTP error: {exc}")
