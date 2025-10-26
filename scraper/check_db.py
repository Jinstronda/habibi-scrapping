"""Quick script to check database contents."""
import sqlite3
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, 'C:\\Users\\joaop\\Documents\\Augusta Labs\\Scrapper for Gui\\scraper')
import config

conn = sqlite3.connect(f"../{config.DB_PATH}")
cursor = conn.cursor()

# Count total records
cursor.execute("SELECT COUNT(*) FROM people")
count = cursor.fetchone()[0]
print(f"\n[OK] Total people in database: {count}")

# Show all records
cursor.execute("SELECT id, name, scraped_at, raw_data FROM people")
rows = cursor.fetchall()

for row in rows:
    print(f"\n{'='*70}")
    print(f"ID: {row[0]}")
    print(f"Name: {row[1]}")
    print(f"Scraped: {row[2]}")
    data = json.loads(row[3])
    print(f"Field count: {data['field_count']}")
    print(f"\nFirst 10 fields:")
    for i, field in enumerate(data['all_fields'][:10], 1):
        print(f"  {i}. {field[:100]}...")  # Truncate long fields

conn.close()
