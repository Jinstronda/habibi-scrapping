"""Clear the attendees database to start fresh."""
import sqlite3
import config
import os

def clear_database():
    """Delete all records from attendees table."""
    if not os.path.exists(config.DB_PATH):
        print(f"Database {config.DB_PATH} doesn't exist yet. Nothing to clear.")
        return

    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    # Get count before deleting
    cursor.execute("SELECT COUNT(*) FROM attendees")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Database is already empty.")
        conn.close()
        return

    # Ask for confirmation
    response = input(f"Are you sure you want to delete {count} attendees? (yes/no): ")

    if response.lower() == 'yes':
        cursor.execute("DELETE FROM attendees")
        conn.commit()
        print(f"✓ Deleted {count} attendees from database.")
        print("Database is now empty. You can run the scraper again.")
    else:
        print("Cancelled. No data deleted.")

    conn.close()

if __name__ == "__main__":
    clear_database()
