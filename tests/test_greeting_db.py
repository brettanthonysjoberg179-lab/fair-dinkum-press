import pytest
from scripts.greetings.db import init_greeting_db, add_contact, get_contacts_by_birthday

def test_greeting_db(tmp_path):
    db_path = tmp_path / "greetings.db"
    conn = init_greeting_db(str(db_path))
    add_contact(conn, "Jane Doe", "jane@example.com", "10-19", "Colleague")
    contacts = get_contacts_by_birthday(conn, "10-19")
    assert len(contacts) == 1
    assert contacts[0]["name"] == "Jane Doe"
    conn.close()
