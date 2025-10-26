# Bug Fix: Duplicate Detection Issue

## The Problem

**Symptom:** Scraper was reporting all attendees as duplicates (already in database), but the database was actually empty.

**Root Cause:** The `_is_within_bounds()` function in `extractor.py` was broken. It just checked if bounds existed, but didn't actually verify if elements were within the specific list item bounds.

**Result:** Every call to `extract_from_list_view(index)` returned the **same first name** from the screen, regardless of which index was requested. So:
- Index 0: Extracted "Ally Zhu"
- Index 1: Extracted "Ally Zhu" (wrong! should be "Joy Zhu")
- Index 2: Extracted "Ally Zhu" (wrong! should be "YU ZHU")
- etc.

After the first save, all subsequent extractions returned "Ally Zhu" again, triggering the duplicate check.

## The Fix

**Changed:** `extract_from_list_view()` now uses uiautomator2's `.child()` method to properly get TextViews from each specific list item:

```python
# OLD (broken):
xml = device.dump_hierarchy()
for elem in root.iter():
    if _is_within_bounds(elem_bounds, bounds):  # Always returned True!
        texts.append(text)

# NEW (fixed):
text_views = item.child(className="android.widget.TextView")
for i in range(text_views.count):
    text = text_views[i].get_text()
    texts.append(text)
```

Now each index correctly extracts from its specific list item.

## How to Test

### 1. Test Extraction (Recommended First Step)

```bash
conda activate turing0.1
cd scraper_attendees
python test_extraction.py
```

**Expected output:**
```
[0] Name: Ally Zhu
    Company-Role: SINGAMAS OFFSHORE CONTAINER & TA...

[1] Name: Joy Zhu
    Company-Role: Jiangyin Furen High Tech Co.,Ltd - Overs...

[2] Name: YU ZHU
    Company-Role: Shanghai Steel Structure Construction (...

[3] Name: JIAJUN ZHU
    Company-Role: Wartsila Gas Solutions Norway AS - Sale...

[4] Name: Haiwen Zhu
    Company-Role: Xecta - Senior Petroleum Engineer
```

**If you see DIFFERENT names**, extraction is working! ✓
**If you see the SAME name repeated**, there's still a bug. ✗

### 2. Clear Database (If Needed)

If you have invalid duplicate data from the bug:

```bash
python clear_db.py
```

Type `yes` to confirm deletion.

### 3. Run the Scraper

```bash
python main.py
```

Now you should see proper output like:
```
✓ Fast: Ally Zhu | SINGAMAS OFFSHORE CONTAINER & TA...
✓ Fast: Joy Zhu | Jiangyin Furen High Tech Co.,Ltd - Overs...
✓ Fast: YU ZHU | Shanghai Steel Structure Construction (...
⚡ Detail: JIAJUN ZHU | Wartsila Gas Solutions Norway AS - Sales Manager
✓ Fast: Haiwen Zhu | Xecta - Senior Petroleum Engineer
```

### 4. Verify Database

```bash
python check_db.py
```

Should show different attendees, not duplicates.

## Additional Changes

1. **Logging level**: Changed from INFO to DEBUG in `utils.py` to show extraction details
2. **Debug output**: Added `logger.debug()` line showing what's extracted at each index
3. **New utilities**:
   - `test_extraction.py` - Test extraction without running full scraper
   - `clear_db.py` - Clear database to start fresh

## Files Modified

- `extractor.py` - Fixed extraction logic (lines 20-49)
- `utils.py` - Changed logging level to DEBUG (line 11)

## Files Added

- `test_extraction.py` - Test script
- `clear_db.py` - Database clearing utility
- `BUGFIX.md` - This file

## Next Steps

1. Run `test_extraction.py` to verify fix works
2. Run `clear_db.py` to clear any bad data
3. Run `main.py` to start scraping with fixed extraction
4. Monitor the log output - you should see different names now!

## Technical Details

The bug was in the bounds checking logic. Android UI elements have bounds in format:
```
bounds="[left,top][right,bottom]"
Example: bounds="[0,374][1080,640]"
```

The old code needed to parse these coordinates and check if the element's bounds were within the parent's bounds, but instead just returned `True` for everything. The new code avoids this entirely by using uiautomator2's built-in `.child()` method which automatically filters to child elements only.
