"""Export database to Excel file."""
import sys
sys.path.insert(0, 'C:\\Users\\joaop\\Documents\\Augusta Labs\\Scrapper for Gui\\scraper')
import sqlite3
import pandas as pd
import json
import config

# Connect to database
conn = sqlite3.connect(config.DB_PATH)

# Read all people from database
df = pd.read_sql_query("SELECT * FROM people", conn)

# Parse raw_data JSON column
if 'raw_data' in df.columns:
    df['field_count'] = df['raw_data'].apply(lambda x: json.loads(x).get('field_count', 0))
    df['all_text'] = df['raw_data'].apply(lambda x: '\n'.join(json.loads(x).get('all_fields', [])))
    df = df.drop('raw_data', axis=1)

# Export to Excel
output_file = "people_data.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Exported {len(df)} people to {output_file}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())

conn.close()
