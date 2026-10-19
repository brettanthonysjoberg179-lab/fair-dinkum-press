# Database and Contact Manager for Greeting Service

import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def init_greeting_db(db_path: str = "data/greetings.db") -> sqlite3.Connection:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            birthday TEXT NOT NULL,
            relationship TEXT
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dispatch_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER,
            occasion TEXT NOT NULL,
            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT,
            FOREIGN KEY (contact_id) REFERENCES contacts (id)
        )
    """)
    conn.commit()
    return conn

def add_contact(conn: sqlite3.Connection, name: str, email: str, birthday: str, relationship: str = ""):
    conn.execute(
        "INSERT INTO contacts (name, email, birthday, relationship) VALUES (?, ?, ?, ?)",
        (name, email, birthday, relationship)
    )
    conn.commit()

def get_contacts_by_birthday(conn: sqlite3.Connection, birthday_mm_dd: str) -> list:
    cursor = conn.execute("SELECT * FROM contacts WHERE birthday = ?", (birthday_mm_dd,))
    return [dict(row) for row in cursor.fetchall()]
