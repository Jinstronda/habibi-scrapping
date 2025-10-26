# Fast Attendees Scraper

I needed to scrape attendee lists. The first version clicked every person. That took forever.

Then I noticed something: most attendees show their full info right in the list. No need to click.

So I built this. It only clicks when the text is cut off with "...". Otherwise it grabs everything from the list view.

Result: **3× faster**. What took 5 minutes now takes 1.7 minutes.

## The Problem

Event apps show attendee lists. Each person has a name and "Company - Role" below it.

Sometimes the role text is too long: "SINGAMAS OFFSHORE CONTAINER & TA..."

Most of the time it's complete: "Xecta - Senior Petroleum Engineer"

The old scraper clicked everyone. Slow.

## The Solution

Fast path: If text is complete, parse it. Don't click. (90% of attendees)

Detail path: If text ends with "...", click for full info. (10% of attendees)

Then I made it faster. Normal extraction makes 7 device calls per person. I switched to batch extraction: dump the entire screen's XML once, parse it locally. Now it's 1 call per 11 people.

Final optimization: reduced timeouts. Android doesn't need 0.3 seconds to respond. 0.01 works fine.

## Setup

You need Python, an Android emulator, and ADB.

```bash
conda activate turing0.1
cd scraper_attendees
pip install -r requirements.txt
```

Open the app to the attendees list. Run:
```bash
python setup.py
```

This dumps the UI structure to `hierarchy.xml`. Look at it. Find the list item selector. Update `config.py`:

```python
APP_PACKAGE = "com.swapcard.apps.android.adipec"  # Your app
LIST_ITEM_SELECTOR = {"resourceId": "com.example:id/item"}
```

## Run It

```bash
python main.py
```

It extracts names, companies, roles. Saves to SQLite. Press Ctrl+C when done.

Want a limit? Edit `config.py`:
```python
MAX_ATTENDEES = 100  # or None for unlimited
```

## Output

Database: `attendees_data.db`

Check it:
```bash
python check_db.py  # Shows stats and recent entries
python export_to_excel.py  # Creates attendees_data.xlsx
```

## Speed

| What | Time per 1000 |
|------|---------------|
| Old scraper (clicks everyone) | 5 minutes |
| This (smart clicking) | 2.1 minutes |
| This + batch extraction | **1.7 minutes** |

Batch extraction is on by default. It dumps the screen XML once instead of making 7 device calls per person.

Turn it off: `USE_BATCH_EXTRACTION = False` in `config.py`

## How It Got Fast

**Problem 1:** Clicking everyone is slow.
**Fix:** Only click truncated entries.

**Problem 2:** Each extraction makes 7 device calls.
**Fix:** Batch extraction - 1 XML dump per screen, parse locally.

**Problem 3:** Conservative timeouts waste time.
**Fix:** `SCROLL_WAIT = 0.01` instead of 0.3.

## Files

```
main.py           # Start here
config.py         # Settings
scraper.py        # Main loop
extractor.py      # Gets names/companies
database.py       # SQLite
```

Functions are short. No complex abstractions. If something breaks, you'll know where.
