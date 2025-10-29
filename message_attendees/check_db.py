"""Quick script to check messages database."""
import sys
import os
# Add message_attendees for local config.py
sys.path.insert(0, os.path.dirname(__file__))
# Add scraper_attendees (not needed here but for consistency)
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import sqlite3
import config

db_path = config.MESSAGES_DB_PATH

if not os.path.exists(db_path):
    print(f"\n[!] Database not found: {db_path}")
    print("Run main.py first to create the database.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Count total records
cursor.execute("SELECT COUNT(*) FROM messages")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM messages WHERE success = 1")
successful = cursor.fetchone()[0]

failed = total - successful

print(f"\n{'='*60}")
print(f"MESSAGE STATISTICS")
print(f"{'='*60}")
print(f"Total messages: {total}")
print(f"Successful: {successful}")
print(f"Failed: {failed}")
print(f"{'='*60}\n")

if total > 0:
    print("Recent messages:\n")
    cursor.execute("""
        SELECT attendee_name, message_text, sent_at, success 
        FROM messages 
        ORDER BY sent_at DESC 
        LIMIT 20
    """)
    rows = cursor.fetchall()
    
    for name, msg, sent_at, success in rows:
        status = "✓" if success else "✗"
        msg_preview = msg[:40] + "..." if len(msg) > 40 else msg
        print(f"{status} {name}")
        print(f"   Message: {msg_preview}")
        print(f"   Sent: {sent_at}\n")

conn.close()

