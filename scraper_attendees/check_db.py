"""Check database contents for attendees scraper."""
import sqlite3
import config

def check_database():
    """Display database statistics and recent entries."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    # Get total count
    cursor.execute("SELECT COUNT(*) FROM attendees")
    total = cursor.fetchone()[0]

    print(f"\n{'='*60}")
    print(f"Attendees Database: {config.DB_PATH}")
    print(f"{'='*60}")
    print(f"Total attendees: {total}")

    if total == 0:
        print("\nDatabase is empty.")
        conn.close()
        return

    # Get truncation statistics
    cursor.execute("SELECT COUNT(*) FROM attendees WHERE is_truncated = 1")
    truncated = cursor.fetchone()[0]
    fast = total - truncated

    print(f"\nExtraction Statistics:")
    print(f"  Fast scraped (from list): {fast} ({fast/total*100:.1f}%)")
    print(f"  Detail scraped (clicked): {truncated} ({truncated/total*100:.1f}%)")

    # Show recent entries
    print(f"\n{'='*60}")
    print("Last 10 attendees:")
    print(f"{'='*60}")

    cursor.execute("""
        SELECT name, company, role, is_truncated
        FROM attendees
        ORDER BY scraped_at DESC
        LIMIT 10
    """)

    for name, company, role, is_truncated in cursor.fetchall():
        marker = "⚡" if is_truncated else "✓"
        print(f"{marker} {name}")
        print(f"  {company} - {role}")
        print()

    conn.close()

if __name__ == "__main__":
    check_database()
