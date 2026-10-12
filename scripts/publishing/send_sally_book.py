import smtplib
import os
from email.message import EmailMessage

TO = "sallybloomfield048@gmail.com"
FROM = "brettanthonysjoberg179@gmail.com"
APP_PASSWORD = "nzjawvvsggfnuryc"
SUBJECT = "A complimentary copy of 'The Autonomous Solopreneur' 📚🚀"

BODY = (
    "Hi Sally,\n\n"
    "Hope you're having a wonderful day!\n\n"
    "I wanted to share a complimentary copy of my newly released masterclass and book, 'The Autonomous Solopreneur: Building & Scaling Multi-Agent AI Enterprises' (published by Fair Dinkum Publishing Agent Workflowz).\n\n"
    "It covers how solo creators and founders can architect 24/7 autonomous AI agent workforces for research, content generation, and headless distribution.\n\n"
    "I've attached both the EPUB ebook and cover art for you to enjoy.\n\n"
    "Lots of love,\n"
    "Brett (Shaggy)"
)

msg = EmailMessage()
msg["From"] = f"Brett Sjoberg <{FROM}>"
msg["To"] = TO
msg["Subject"] = SUBJECT
msg.set_content(BODY, subtype="plain", charset="utf-8")

# Attach EPUB
epub_path = "outputs/the_autonomous_solopreneur.epub"
if os.path.exists(epub_path):
    with open(epub_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="epub+zip", filename="The_Autonomous_Solopreneur.epub")

# Attach Cover
cover_path = "outputs/autonomous_solopreneur_cover.png"
if os.path.exists(cover_path):
    with open(cover_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename="Autonomous_Solopreneur_Cover.png")

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
        s.login(FROM, APP_PASSWORD)
        s.send_message(msg)
    print(f"Successfully sent complimentary copy to {TO}")
except Exception as exc:
    print(f"SMTP error: {type(exc).__name__} {exc}")
