# Attendees Scraper - Design-Based Updates

## What Was Updated

All files have been updated based on the actual attendees page design from the screenshots.

### ✅ Design Analysis

**List View Structure:**
- Name displayed in bold (e.g., "Ally Zhu", "Joy Zhu")
- Company-Role text below in gray (e.g., "Xecta - Senior Petroleum Engineer")
- Truncated entries end with "..." (e.g., "SINGAMAS OFFSHORE CONTAINER & TA...")

**Detail Page Structure (when clicked):**
- "Company Name" label followed by full company text
- "Job Title" label followed by full role text
- Additional fields: Country, Job Function, Seniority

### 📝 Updated Files

1. **extractor.py** - Complete rewrite
   - `extract_from_list_view()`: Gets name + company-role from list XML
   - `extract_from_detail_page()`: Gets full company + job title from detail page
   - `is_truncated()`: Checks if text ends with "..."
   - `parse_company_role()`: Splits "Company - Role" format

2. **scraper.py** - Updated extraction flow
   - Uses new extractor functions
   - Fast path: Parse and save directly when not truncated
   - Detail path: Click, extract full data, back, save when truncated
   - Better logging with ✓ (fast) and ⚡ (detail) markers

3. **config.py** - Simplified and documented
   - Removed unused selectors
   - Added clear comments explaining list/detail structure
   - APP_PACKAGE already correct: "com.swapcard.apps.android.adipec"

4. **database.py** - Attendees schema
   - Simple table: name, company, role, is_truncated, scraped_at
   - Tracks which extraction method was used

5. **utils.py** - Updated log filename
   - Changed from 'scraper.log' to 'attendees_scraper.log'

6. **check_db.py** - NEW utility
   - Shows total attendees count
   - Fast vs Detail extraction statistics
   - Last 10 scraped entries

7. **requirements.txt** - Added dependencies
   - pandas>=2.0.0 (for Excel export)
   - openpyxl>=3.0.0 (for Excel export)

8. **README.md** - Updated with actual design info
   - Clear explanation of list vs detail view structure
   - Examples from actual screenshots
   - Complete usage instructions

## How The Scraper Works

### Smart Fast-Path Logic

```
For each attendee:
  ├─ Extract from list: Name + "Company - Role"
  ├─ Check database: Skip if already exists
  └─ Check truncation: Does text end with "..."?
      ├─ NO  → Parse "Company - Role" → Save (0.3s) ✓ FAST
      └─ YES → Click → Extract detail → Back → Save (1.5s) ⚡ DETAIL
```

### Expected Performance

For 1000 attendees with 5% truncated:
- **Fast path**: 950 attendees × 0.3s = 4.75 minutes
- **Detail path**: 50 attendees × 1.5s = 1.25 minutes
- **Total**: ~6 minutes (vs ~25 minutes clicking all)

## Next Steps

### 1. Install Dependencies
```bash
conda activate turing0.1
cd scraper_attendees
pip install -r requirements.txt
```

### 2. Run Setup (Optional)
```bash
python setup.py
```
This dumps the current UI hierarchy to verify selectors are correct.

### 3. Verify Config
Check `config.py` has correct values:
- `APP_PACKAGE = "com.swapcard.apps.android.adipec"` ✓
- `LIST_ITEM_SELECTOR` points to attendee rows ✓

### 4. Run Scraper
```bash
python main.py
```
Watch the log output:
- ✓ = Fast scraped (from list)
- ⚡ = Detail scraped (clicked for full data)

### 5. Check Progress
```bash
python check_db.py
```
Shows statistics and recent entries.

### 6. Export to Excel
```bash
python export_to_excel.py
```
Creates `attendees_data.xlsx` with all data.

## Files Created (12 total)

```
scraper_attendees/
├── main.py              ✓ Entry point
├── config.py            ✓ Configuration (updated)
├── database.py          ✓ Attendees schema
├── scraper.py           ✓ Fast-path logic (updated)
├── extractor.py         ✓ List + detail extraction (updated)
├── device.py            ✓ Device connection
├── utils.py             ✓ Utilities (updated log name)
├── setup.py             ✓ UI inspection
├── check_db.py          ✓ Database viewer (NEW)
├── export_to_excel.py   ✓ Excel export
├── requirements.txt     ✓ Dependencies (updated)
└── README.md            ✓ Documentation (updated)
```

## Key Differences from People Scraper

| Feature | People Scraper | Attendees Scraper |
|---------|---------------|-------------------|
| Data source | Always clicks into detail | List view + conditional detail |
| Speed | ~1.5s per person | ~0.3s per attendee (mostly) |
| Database | JSON blob with all fields | Simple: name, company, role |
| Stop condition | Name marker check | Manual (Ctrl+C or MAX_ATTENDEES) |
| "Show More" | Always clicks button | Not needed |
| Scrolling | Checks for exact marker | Continues until stopped |

## Troubleshooting

### If extraction fails:
1. Run `python setup.py` to dump UI hierarchy
2. Open `hierarchy.xml`
3. Verify structure matches expectations
4. Check `LIST_ITEM_SELECTOR` in config.py

### If clicking fails:
- Increase `PAGE_LOAD_TIMEOUT` in config.py
- Check device connection with `adb devices`
- View error screenshots in `screenshots_attendees/`

### If parsing fails:
- Check if "Company - Role" format is different
- Update `parse_company_role()` in extractor.py
- Verify truncation marker is "..." (not "…" or other)

## All functions <25 lines ✓

Every function follows the CLAUDE.md guideline:
- `extract_from_list_view()`: 19 lines
- `extract_from_detail_page()`: 18 lines
- `scrape_single_attendee()`: 24 lines
- `parse_company_role()`: 4 lines
- `is_truncated()`: 2 lines

Clean, focused, maintainable code!
