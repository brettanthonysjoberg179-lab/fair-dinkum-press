import os
import sqlite3
from datetime import datetime

DEFAULT_DB_PATH = "data/business.db"

def get_db_connection(db_path=None):
    """Get a SQLite connection with WAL mode and row factory enabled."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db(db_path=None):
    """Initialize database schema tables if they do not exist."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        agent TEXT NOT NULL,
        action TEXT NOT NULL,
        status TEXT NOT NULL,
        details TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        company TEXT,
        status TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS content_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        title TEXT NOT NULL,
        url TEXT,
        type TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saas_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        metric_name TEXT NOT NULL,
        value REAL NOT NULL,
        details TEXT
    )
    """)
    
    conn.commit()
    return conn

def log_agent_action(conn, agent, action, status, details=""):
    """Log an agent action execution."""
    timestamp = datetime.now().isoformat()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO agent_logs (timestamp, agent, action, status, details) VALUES (?, ?, ?, ?, ?)",
        (timestamp, agent, action, status, details)
    )
    conn.commit()

def save_lead(conn, name, email, company="", status="New"):
    """Save or update a lead record."""
    timestamp = datetime.now().isoformat()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leads (timestamp, name, email, company, status) VALUES (?, ?, ?, ?, ?)",
        (timestamp, name, email, company, status)
    )
    conn.commit()

def save_content_record(conn, title, url, type, status="Draft"):
    """Save content publication record."""
    timestamp = datetime.now().isoformat()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO content_records (timestamp, title, url, type, status) VALUES (?, ?, ?, ?, ?)",
        (timestamp, title, url, type, status)
    )
    conn.commit()

def save_saas_metric(conn, metric_name, value, details=""):
    """Save SaaS operational metric."""
    timestamp = datetime.now().isoformat()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO saas_metrics (timestamp, metric_name, value, details) VALUES (?, ?, ?, ?, ?)",
        (timestamp, metric_name, value, details)
    )
    conn.commit()
