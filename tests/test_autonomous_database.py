import os
import sqlite3
import pytest
from scripts.autonomous.database import init_db, get_db_connection, log_agent_action, save_lead, save_content_record

def test_database_init_and_logging(tmp_path):
    db_path = tmp_path / "test_business.db"
    conn = init_db(str(db_path))
    assert conn is not None
    
    log_agent_action(conn, "PublishingAgent", "KeywordScrape", "Success", "Found 5 new keywords")
    cursor = conn.cursor()
    cursor.execute("SELECT agent, action, status FROM agent_logs")
    row = cursor.fetchone()
    assert tuple(row) == ("PublishingAgent", "KeywordScrape", "Success")
    assert row["agent"] == "PublishingAgent"
    conn.close()

def test_save_lead_and_content(tmp_path):
    db_path = tmp_path / "test_business.db"
    conn = init_db(str(db_path))
    
    save_lead(conn, "Jane Doe", "jane@example.com", "Acme Corp", "Qualified")
    save_content_record(conn, "AI Trends", "https://example.com/ai-trends", "Blog", "Published")
    
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM leads")
    lead_row = cursor.fetchone()
    assert tuple(lead_row) == ("Jane Doe", "jane@example.com")
    
    cursor.execute("SELECT title, type FROM content_records")
    content_row = cursor.fetchone()
    assert tuple(content_row) == ("AI Trends", "Blog")
    conn.close()
