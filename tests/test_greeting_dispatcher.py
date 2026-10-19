import pytest
from scripts.greetings.dispatcher import render_greeting_email, dispatch_greeting

def test_template_rendering():
    email = render_greeting_email("birthday", "Jane", "Alice", "Great colleague")
    assert "Jane" in email["subject"]
    assert "Alice" in email["body"]
    assert "professional" in email["body"].lower() or "success" in email["body"].lower() or "fulfilling birthday" in email["body"].lower()

def test_dispatch_greeting():
    res = dispatch_greeting("jane@example.com", "christmas", "Jane", "Alice", "Key partner", dry_run=True)
    assert res["status"] == "sent"
    assert res["recipient"] == "jane@example.com"
    assert "Christmas" in res["subject"]
