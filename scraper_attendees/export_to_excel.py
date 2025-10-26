"""Export attendees database to Excel file."""
import sys
sys.path.insert(0, 'C:\\Users\\joaop\\Documents\\Augusta Labs\\Scrapper for Gui\\scraper_attendees')
import sqlite3
import pandas as pd
import config

# Connect to database
conn = sqlite3.connect(config.DB_PATH)

# Read all attendees from database
df = pd.read_sql_query("SELECT * FROM attendees", conn)

# Convert is_truncated from 0/1 to False/True
if 'is_truncated' in df.columns:
    df['is_truncated'] = df['is_truncated'].astype(bool)

# Export to Excel
output_file = "attendees_data.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Exported {len(df)} attendees to {output_file}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())

# Statistics
if len(df) > 0:
    truncated_count = df['is_truncated'].sum() if 'is_truncated' in df.columns else 0
    print(f"\nStatistics:")
    print(f"  Total attendees: {len(df)}")
    print(f"  Truncated (needed detail page): {truncated_count}")
    print(f"  Fast scraped (from list): {len(df) - truncated_count}")

conn.close()
