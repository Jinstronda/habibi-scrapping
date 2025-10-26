# Android App Scrapers

I needed to extract data from an Android event app. Two types of data: detailed people profiles and quick attendee lists.

Different use cases need different tools.

## scraper/ - People Scraper

Clicks every person. Gets everything. Stores it all.

Use this when you need complete profiles with all fields.

**Speed:** 1.5s per person

**Database:** JSON blob with all extracted text

**Stop condition:** Reaches a specific name marker

## scraper_attendees/ - Fast Attendees Scraper

Only clicks truncated entries. Most data is visible in the list.

Use this when you just need names, companies, and roles.

**Speed:** 0.10s per person (3× faster)

**Database:** Simple schema - name, company, role

**Stop condition:** Manual (Ctrl+C)

## The Difference

People scraper extracts complete profiles. Every field. Structured data.

Attendees scraper is optimized for speed. It noticed that most attendee info is already visible in the list view. Why click when you don't need to?

Then I optimized it further. Normal extraction makes 7 device calls per person. I switched to batch extraction: dump the entire screen once, parse it locally. Now it's 1 call per 11 people.

## Setup

Both use the same approach:

1. Run `python setup.py` while the app is open
2. Update `config.py` with the correct element selectors
3. Run `python main.py`

The scrapers handle:
- Scrolling
- Duplicate detection
- Error recovery with screenshots
- SQLite storage

## Results

1000 people with people scraper: 25 minutes
1000 attendees with attendees scraper: 1.7 minutes

Choose based on what you need. Complete data or quick extraction.

---

# People Scraper Details

I needed complete profiles. Every field. Everything the app shows when you click someone.

This scraper clicks every person, presses "show more", and extracts all visible text.

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

---

# Fast Attendees Scraper Details

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
