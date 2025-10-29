"""Show database path and check if it exists."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import config

print(f"Messages DB path: {config.MESSAGES_DB_PATH}")
print(f"Exists: {os.path.exists(config.MESSAGES_DB_PATH)}")

if os.path.exists(config.MESSAGES_DB_PATH):
    # Delete it
    import sqlite3
    conn = sqlite3.connect(config.MESSAGES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    count = cursor.rowcount
    conn.close()
    print(f"[OK] Cleared {count} records from messages table")
else:
    print("No database file found - it will be created fresh on next run")

