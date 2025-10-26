# People Scraper

I needed complete profiles. Every field. Everything the app shows when you click someone.

This scraper clicks every person, presses "show more", and extracts all visible text.

Use this when you need the full dataset. Not just names and titles, but everything.

**Speed:** 1.5s per person

**Database:** JSON blob containing all extracted fields

**Stop condition:** Reaches a specific name marker

## The Approach

The app shows a list of people. Click one, you get their profile. Click "show more", you see everything.

So that's what this does. Iterate through the list, click each person, expand the details, save everything.

It stores the data as a JSON blob. No schema guessing. Whatever the app shows, we capture.

## Setup

You need Python, an Android emulator, and ADB.

```bash
conda activate turing0.1
cd scraper
pip install -r requirements.txt
```

Open the app to the people list. Run:
```bash
python setup.py
```

This dumps the UI structure to `hierarchy.xml`. Look at it. Find the list item selector and the "show more" button. Update `config.py`:

```python
APP_PACKAGE = "com.swapcard.apps.android.adipec"  # Your app
LIST_ITEM_SELECTOR = {"resourceId": "com.example:id/item"}
SHOW_MORE_BUTTON = {"text": "show more"}  # Or whatever it says
```

## Run It

```bash
python main.py
```

It clicks each person. Presses "show more". Extracts everything. Saves to SQLite.

The scraper stops when it reaches a specific name you set in `config.py`:

```python
STOP_MARKER = "Your Name Here"  # When it hits this name, it stops
```

## Output

Database: `people_data.db`

Each person gets stored with:
- Name
- Timestamp
- Raw JSON containing all extracted text fields

Check it:
```python
import sqlite3
import json

conn = sqlite3.connect('people_data.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM people")
for row in cursor.fetchall():
    print(f"\nName: {row[1]}")
    data = json.loads(row[3])
    print(f"Fields: {data['all_fields']}")
```

## Files

```
main.py           # Start here
config.py         # Settings
scraper.py        # Main loop
extractor.py      # Gets all visible text
database.py       # SQLite
```

Functions are short. No complex abstractions. If something breaks, you'll know where.
