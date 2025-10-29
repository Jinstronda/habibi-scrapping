"""Database operations for message tracking and attendee reading."""
import sys
import os
# Add message_attendees for local config.py
sys.path.insert(0, os.path.dirname(__file__))
# Add scraper_attendees for device.py and utils.py (if needed)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import sqlite3
from datetime import datetime
import config

def init_messages_db():
    """Initialize messages tracking database."""
    conn = sqlite3.connect(config.MESSAGES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attendee_name TEXT UNIQUE,
            message_text TEXT,
            sent_at TIMESTAMP,
            success INTEGER
        )
    """)
    conn.commit()
    conn.close()

def message_already_sent(name):
    """Check if message already sent to this attendee."""
    conn = sqlite3.connect(config.MESSAGES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM messages WHERE attendee_name = ?", (name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_message_record(name, message, success):
    """Save message sending record."""
    conn = sqlite3.connect(config.MESSAGES_DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO messages (attendee_name, message_text, sent_at, success)
            VALUES (?, ?, ?, ?)
        """, (name, message, datetime.now(), 1 if success else 0))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def read_attendees_from_file(filepath):
    """Read attendee names from text file (one per line)."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]
    return names

def read_all_attendees_from_db():
    """Read all attendee names from scraper database."""
    if not os.path.exists(config.ATTENDEES_DB_PATH):
        return []
    conn = sqlite3.connect(config.ATTENDEES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM attendees ORDER BY name")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names

def get_attendees_to_message():
    """Get list of attendees based on config."""
    if config.USE_TEST_LIST:
        return read_attendees_from_file(config.TEST_LIST_FILE)
    return read_all_attendees_from_db()

def get_message_stats():
    """Get statistics about sent messages."""
    conn = sqlite3.connect(config.MESSAGES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(success) FROM messages")
    total, successful = cursor.fetchone()
    conn.close()
    return total or 0, successful or 0

