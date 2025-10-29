"""Clear messages database to start fresh."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import config

if os.path.exists(config.MESSAGES_DB_PATH):
    os.remove(config.MESSAGES_DB_PATH)
    print(f"[OK] Deleted {config.MESSAGES_DB_PATH}")
    print("Database cleared! You can now run main.py to message everyone again.")
else:
    print("No messages database found.")

