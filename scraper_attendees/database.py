"""Database operations for scraped attendees."""
import sqlite3
from datetime import datetime
import config

def init_db():
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            company TEXT,
            role TEXT,
            is_truncated INTEGER,
            scraped_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def attendee_exists(name):
    """Check if attendee already scraped."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM attendees WHERE name = ?", (name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_attendee(name, company, role, is_truncated):
    """Save attendee data to database."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO attendees (name, company, role, is_truncated, scraped_at)
            VALUES (?, ?, ?, ?, ?)
        """, (name, company, role, 1 if is_truncated else 0, datetime.now()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_attendees():
    """Retrieve all scraped attendees."""
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendees ORDER BY scraped_at DESC")
    attendees = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return attendees

def get_attendees_count():
    """Get total count of attendees in database."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendees")
    count = cursor.fetchone()[0]
    conn.close()
    return count
