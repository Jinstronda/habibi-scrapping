# Android App Scraper

Automated scraper for extracting data from Android apps using uiautomator2.

## Features

- Automatic list iteration with scrolling
- Clicks "show more" button to expand all data
- Extracts all visible text and metadata
- SQLite database storage with deduplication
- Error handling with screenshots
- Retry logic for flaky operations

## Prerequisites

1. Android emulator running (or physical device connected)
2. ADB installed and in PATH
3. Conda environment: `turing0.1`
4. USB debugging enabled on device

## Installation

```bash
conda activate turing0.1
cd scraper
pip install -r requirements.txt
```

## Setup

### Step 1: Find App Package Name and UI Elements

1. Start your Android emulator
2. Open the target app
3. Navigate to the screen with the list of people
4. Run setup script:

```bash
python setup.py
```

This will:
- Identify the app package name
- Dump UI hierarchy to `hierarchy.xml`
- Show you what to configure

### Step 2: Configure Selectors

Open `config.py` and update:

```python
APP_PACKAGE = "com.example.app"  # From setup.py output
LIST_ITEM_SELECTOR = {"resourceId": "com.example:id/person_item"}  # From hierarchy.xml
SHOW_MORE_BUTTON = {"text": "show more"}  # Adjust if different
```

**Finding selectors in hierarchy.xml:**
- Look for repeating elements (list items)
- Check attributes: `resource-id`, `class`, `text`, `content-desc`
- Common patterns:
  - `{"resourceId": "com.app:id/element"}`
  - `{"className": "android.widget.TextView"}`
  - `{"text": "Show More", "className": "android.widget.Button"}`

## Usage

```bash
python main.py
```

The scraper will:
1. Connect to emulator
2. Iterate through list items
3. Click each person
4. Click "show more" button
5. Extract all visible data
6. Press back button
7. Save to SQLite database
8. Continue until list is exhausted

## Output

- **Database:** `people_data.db` (SQLite)
- **Logs:** `scraper.log`
- **Screenshots:** `screenshots/` (on errors)

### Viewing Data

```python
import sqlite3
import json

conn = sqlite3.connect('people_data.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM people")
for row in cursor.fetchall():
    print(f"\nName: {row[1]}")
    print(f"Scraped: {row[2]}")
    data = json.loads(row[3])
    print(f"Fields: {data['all_fields']}")
```

## Configuration Options

Edit `config.py` to adjust:

- **Timeouts:** `CLICK_TIMEOUT`, `PAGE_LOAD_TIMEOUT`, `SCROLL_WAIT`
- **Retries:** `MAX_RETRIES`
- **Screenshots:** `SAVE_SCREENSHOTS_ON_ERROR`
- **Database:** `DB_PATH`

## Troubleshooting

### "No device connected"
```bash
adb devices
# If empty, restart emulator or run:
adb kill-server && adb start-server
```

### "Element not found"
- Run `setup.py` again to dump UI hierarchy
- Check `hierarchy.xml` for correct selectors
- Update `config.py` with accurate resource IDs

### "Show more button not found"
- Check button text in app (case-sensitive)
- Update `SHOW_MORE_BUTTON` in config.py
- Try different selector strategies (resourceId, className)

### App crashes during scraping
- Increase timeouts in config.py
- Check logs in `scraper.log`
- View error screenshots in `screenshots/`

## Project Structure

```
scraper/
├── main.py           # Entry point
├── setup.py          # Setup wizard
├── config.py         # Configuration
├── device.py         # Device connection
├── scraper.py        # List iteration logic
├── extractor.py      # Data extraction
├── database.py       # SQLite operations
├── utils.py          # Helper functions
└── requirements.txt  # Dependencies
```

## Code Guidelines

- All functions <25 lines (CLAUDE.md compliance)
- DRY principle enforced
- Retry logic for reliability
- Comprehensive error handling

## Next Steps

1. Run `setup.py` to identify your app
2. Update `config.py` with selectors
3. Test with `python main.py`
4. Adjust selectors if needed
5. Let it run to scrape all data
