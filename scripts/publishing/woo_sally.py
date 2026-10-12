import smtplib
from email.message import EmailMessage

TO = "sallybloomfield048@gmail.com"
FROM = "brettanthonysjoberg179@gmail.com"
APP_PASSWORD = "nzjawvvsggfnuryc"
SUBJECT = "Thinking of you (and completely offline for once) ✨"

BODY = (
    "Hi Sally,\n\n"
    "I was sitting here designing autonomous AI agent swarms and automating digital publishing pipelines, but somehow my mind kept wandering away from code and straight back to you.\n\n"
    "It turns out that even with all the machine intelligence in the world, my favorite algorithm still revolves completely around you.\n\n"
    "I hope your day is as wonderful, bright, and captivating as you are. Let’s grab coffee or dinner soon—my heart doesn't need an agent to know it wants to spend time with you.\n\n"
    "Lots of love,\n"
    "Brett (Shaggy)"
)

def send_email():
    msg = EmailMessage()
    msg["From"] = f"Brett Sjoberg <{FROM}>"
    msg["To"] = TO
    msg["Subject"] = SUBJECT
    msg.set_content(BODY, subtype="plain", charset="utf-8")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
            s.login(FROM, APP_PASSWORD)
            s.send_message(msg)
        print(f"Successfully sent romantic email to Sally ({TO})!")
    except Exception as exc:
        print(f"SMTP error: {exc}")

if __name__ == "__main__":
    send_email()
