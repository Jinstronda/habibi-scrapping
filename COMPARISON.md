# Scraper Comparison: People vs Attendees

## Quick Reference

| Aspect | scraper/ (People) | scraper_attendees/ (Attendees) |
|--------|------------------|-------------------------------|
| **Data Location** | Only in detail page | List view + detail (if truncated) |
| **Clicking** | Every person | Only when text ends with "..." |
| **Speed** | ~1.5s per person | ~0.3s per attendee (90% of time) |
| **Database** | JSON blob with all fields | Simple: name, company, role, is_truncated |
| **Stop Logic** | Name marker ("Shengli Oilfield") | Manual (Ctrl+C) or MAX_ATTENDEES |
| **"Show More"** | Always clicks expand button | Not needed |
| **Use Case** | Full profile extraction | Quick contact list |

## Speed Comparison

### People Scraper (scraper/)
```
For 1000 people:
1000 × 1.5s = 25 minutes
(Every person requires click → show more → extract → back)
```

### Attendees Scraper (scraper_attendees/)
```
For 1000 attendees (5% truncated):
- 950 fast   × 0.3s = 4.75 min  ✓
- 50 detail  × 1.5s = 1.25 min  ⚡
Total: ~6 minutes (4× faster!)
```

## When to Use Each

### Use People Scraper (scraper/) when:
- Need all profile details (Country, Job Function, Seniority, etc.)
- Want structured data with all fields
- Have a specific end marker (person name)
- Time is not critical

### Use Attendees Scraper (scraper_attendees/) when:
- Only need name, company, and role
- Speed is priority
- Most data is visible in list view
- Want to process quickly and export to Excel

## Architecture Differences

### People Scraper Flow
```
Connect → For each item:
  ├─ Click person
  ├─ Click "show more" button
  ├─ Extract all text from detail page
  ├─ Press back
  ├─ Save to database (raw JSON)
  └─ Check if reached end marker → Stop or Continue
```

### Attendees Scraper Flow
```
Connect → For each item:
  ├─ Extract name + company-role from list
  ├─ Check if ends with "..."
  │   ├─ NO  → Parse & save directly ✓ (FAST)
  │   └─ YES → Click → Extract detail → Back → Save ⚡
  └─ Continue until Ctrl+C or limit reached
```

## Database Schemas

### People (scraper/)
```sql
CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    scraped_at TIMESTAMP,
    raw_data TEXT  -- JSON: {"all_fields": [...], "field_count": N}
)
```

### Attendees (scraper_attendees/)
```sql
CREATE TABLE attendees (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    company TEXT,
    role TEXT,
    is_truncated INTEGER,  -- 0=fast, 1=detail
    scraped_at TIMESTAMP
)
```

## Code Structure Comparison

Both follow same modular pattern:

```
main.py           # Entry point
config.py         # Configuration
device.py         # Device connection
database.py       # SQLite operations
scraper.py        # Main scraping loop
extractor.py      # Data extraction logic
utils.py          # Helpers (logging, screenshots)
setup.py          # UI inspection tool
export_to_excel.py # Excel export
check_db.py       # Database viewer
```

## Key Configuration Differences

### People Scraper (scraper/config.py)
```python
SHOW_MORE_BUTTON = {...}  # Clicks to expand
BACK_BUTTON_METHOD = "press_back"
# Stop condition in scraper.py: name.startswith("Shengli Oilfield")
```

### Attendees Scraper (scraper_attendees/config.py)
```python
MAX_ATTENDEES = None  # Optional limit
# No show more button needed
# No automatic stop condition
```

## Performance Metrics

### People Scraper
- **Time per person**: ~1.5s
- **Success rate**: High (all data extracted)
- **Data completeness**: 100% (all fields)
- **Best for**: Complete profiles

### Attendees Scraper
- **Time per attendee**: ~0.3s (fast) or ~1.5s (detail)
- **Fast path rate**: ~90-95%
- **Data completeness**: Name, Company, Role (essential fields)
- **Best for**: Quick contact lists

## Running Both Scrapers

Both can run independently:

```bash
# People scraper
cd scraper
python main.py

# Attendees scraper (separate database)
cd ../scraper_attendees
python main.py
```

They use different:
- Databases: `people_data.db` vs `attendees_data.db`
- Log files: `scraper.log` vs `attendees_scraper.log`
- Screenshots: `screenshots/` vs `screenshots_attendees/`

## Choosing the Right Scraper

**Quick decision tree:**

1. Do you need full profiles with all fields?
   - YES → Use `scraper/` (People)
   - NO → Continue

2. Is most data visible in list view?
   - YES → Use `scraper_attendees/` (Attendees)
   - NO → Use `scraper/` (People)

3. Is speed critical?
   - YES → Use `scraper_attendees/` (Attendees)
   - NO → Either works

4. Do you have a clear end marker?
   - YES → Use `scraper/` (People)
   - NO → Use `scraper_attendees/` (Attendees)

## Example Use Cases

### People Scraper Best For:
- Extracting 100 VIP contacts with full details
- Building complete profile database
- When you know exact endpoint ("last person")
- Research requiring all data fields

### Attendees Scraper Best For:
- Quick scan of 1000+ attendees
- Building contact list for email campaign
- When you just need "who works where"
- Speed matters more than completeness

## Summary

Both scrapers share the same solid foundation but optimized for different use cases:

- **People scraper**: Thorough, complete, slower
- **Attendees scraper**: Fast, essential data, optimized

Choose based on your specific needs!
