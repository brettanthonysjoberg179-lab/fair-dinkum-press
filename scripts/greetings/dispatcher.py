# Warm and Professional Greeting Dispatcher and Templates

import logging

logger = logging.getLogger(__name__)

OCCASION_TEMPLATES = {
    "birthday": {
        "subject": "Warmest wishes on your birthday, {recipient_name}!",
        "body": "Dear {recipient_name},\n\nWishing you a wonderful and fulfilling birthday! As you celebrate another year, I want to express my appreciation for our relationship ({relationship_note}). May this coming year bring you continued professional success, personal joy, and good health.\n\nWarm regards,\n{sender_name}"
    },
    "christmas": {
        "subject": "Season's Greetings & Warm Wishes for Christmas, {recipient_name}",
        "body": "Dear {recipient_name},\n\nAs the year draws to a close, I wanted to send my warmest thoughts for the holiday season. Thank you for wonderful collaboration and connection this year ({relationship_note}). Wishing you a peaceful, joyful Christmas and a prosperous New Year.\n\nWarmly,\n{sender_name}"
    },
    "easter": {
        "subject": "Happy Easter & Warm Spring Wishes, {recipient_name}",
        "body": "Dear {recipient_name},\n\nWishing you a joyful Easter filled with renewal, peace, and moments of relaxation with your loved ones. It is a pleasure working/connecting with you ({relationship_note}).\n\nBest regards,\n{sender_name}"
    },
    "valentines": {
        "subject": "Appreciation & Warm Regards on Valentine's Day, {recipient_name}",
        "body": "Dear {recipient_name},\n\nOn this day of appreciation, I want to send a brief note to thank you for your incredible support and partnership ({relationship_note}). Working with you is truly a privilege.\n\nWith warm regards,\n{sender_name}"
    },
    "halloween": {
        "subject": "Wishing you a wonderful autumn and spooky season, {recipient_name}",
        "body": "Dear {recipient_name},\n\nI hope you are enjoying a fantastic autumn season! Sending warm wishes for a delightful and festive Halloween ({relationship_note}).\n\nBest regards,\n{sender_name}"
    }
}

def render_greeting_email(occasion: str, recipient_name: str, sender_name: str, relationship_note: str = "") -> dict:
    if occasion not in OCCASION_TEMPLATES:
        raise ValueError(f"Unknown occasion: {occasion}")
    
    template = OCCASION_TEMPLATES[occasion]
    note = relationship_note or "valued connection"
    
    subject = template["subject"].format(recipient_name=recipient_name)
    body = template["body"].format(
        recipient_name=recipient_name,
        sender_name=sender_name,
        relationship_note=note
    )
    
    return {"subject": subject, "body": body}

def dispatch_greeting(recipient_email: str, occasion: str, recipient_name: str, sender_name: str, relationship_note: str = "", dry_run: bool = True) -> dict:
    email = render_greeting_email(occasion, recipient_name, sender_name, relationship_note)
    logger.info(f"[{'DRY-RUN'}] Dispatching {occasion} greeting to {recipient_email} ({recipient_name})")
    return {
        "status": "sent",
        "recipient": recipient_email,
        "occasion": occasion,
        "subject": email["subject"],
        "body": email["body"],
        "dry_run": dry_run
    }
