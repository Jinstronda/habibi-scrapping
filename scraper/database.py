"""Database operations for scraped data."""
import sqlite3
import json
from datetime import datetime
import config

def init_db():
    """Initialize SQLite database with schema."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            scraped_at TIMESTAMP,
            raw_data TEXT
        )
    """)
    conn.commit()
    conn.close()

def person_exists(name):
    """Check if person already scraped."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM people WHERE name = ?", (name,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def save_person(name, data):
    """Save person data to database."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO people (name, scraped_at, raw_data)
            VALUES (?, ?, ?)
        """, (name, datetime.now(), json.dumps(data)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_people():
    """Retrieve all scraped people."""
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people ORDER BY scraped_at DESC")
    people = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return people

def get_people_count():
    """Get total count of people in database."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM people")
    count = cursor.fetchone()[0]
    conn.close()
    return count
