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
