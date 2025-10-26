# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

**Required Conda Environment:** `turing0.1`

Always activate before running any Python scripts:
```bash
conda activate turing0.1
```

## Essential Commands

### Setup and Installation
```bash
# Install dependencies
cd scraper
pip install -r requirements.txt

# Initial setup - identifies app package and dumps UI hierarchy
python setup.py
```

### Running the Scraper
```bash
# Main scraper entry point
python main.py

# Export scraped data to Excel
python export_to_excel.py

# Check database contents
python check_db.py
```

### Development Utilities
```bash
# Inspect UI hierarchy of current screen
python inspect_detail.py

# Get precise coordinates for list items
python get_coordinates.py
python get_precise_coords.py
```

## Architecture Overview

This is an **Android app scraper** using `uiautomator2` to automate data extraction from Android applications. The scraper operates by iterating through list items, clicking each one, expanding details, extracting text, and saving to SQLite.

### Core Data Flow

1. **Device Connection** (`device.py`) → Establishes connection to Android emulator/device
2. **List Iteration** (`scraper.py`) → Scrolls through list, clicks items by index/coordinates
3. **Data Extraction** (`extractor.py`) → Clicks "show more" buttons, dumps UI hierarchy, extracts all text
4. **Storage** (`database.py`) → Saves to SQLite with deduplication by name
5. **Export** (`export_to_excel.py`) → Converts database to Excel format

### Module Responsibilities

- **`main.py`**: Entry point, orchestrates initialization and scraping loop
- **`config.py`**: Central configuration - timeouts, selectors, coordinates, app package
- **`device.py`**: Device connection and management via uiautomator2
- **`scraper.py`**: Main scraping logic - list iteration, scrolling, retry logic
- **`extractor.py`**: Detail page data extraction - clicks "show more", scrolls, dumps XML, extracts text
- **`database.py`**: SQLite operations - schema init, deduplication, CRUD operations
- **`utils.py`**: Logging, retry decorator, screenshot utilities
- **`setup.py`**: Initial app inspection and UI hierarchy dumping

### Key Design Patterns

**Element Selection Strategy**: Uses both element selectors (resourceId) and hard-coded coordinates (`ITEM_COORDINATES`) as fallback when element references become stale during scrolling.

**Scroll Mechanism**: After processing 11 items (indices 0-10), scrolls backward on list container and resets index to 0. Continues until stop condition (specific name marker).

**Deduplication**: Checks `person_exists(name)` before saving to avoid duplicate entries across interrupted runs.

**Error Handling**: Screenshots saved on errors to `screenshots/` directory. Retry logic via `@retry_on_failure` decorator for flaky operations.

## Configuration Workflow

### 1. Initial Setup
1. Start Android emulator
2. Open target app and navigate to list screen
3. Run `python setup.py` to identify package name and dump UI
4. Open generated `hierarchy.xml` to inspect UI structure

### 2. Update config.py
- Set `APP_PACKAGE` from setup.py output
- Find repeating list item elements in hierarchy.xml
- Update `LIST_ITEM_SELECTOR` with resourceId or className
- Update `SHOW_MORE_BUTTON` selector for detail page
- Adjust `ITEM_COORDINATES` if using coordinate-based clicking

### 3. Fine-Tuning
- **Timeouts**: Reduce `CLICK_TIMEOUT`, `PAGE_LOAD_TIMEOUT`, `SCROLL_WAIT` for speed (currently maximized)
- **Stop Condition**: Modify `scraper.py:56` if end marker name changes
- **Scroll Count**: Adjust `index == 11` in `scraper.py:69` based on items visible per screen

## Critical Implementation Notes

### Function Size Constraint
All functions **MUST be <25 lines of code** per CLAUDE.md user guidelines. When refactoring or adding features, break into small, single-purpose functions.

### DRY Enforcement
Before writing any new function:
1. Search for existing implementations in codebase
2. Check `utils.py` for reusable utilities
3. Consolidate duplicate logic immediately

### Coordinate-Based Clicking
`ITEM_COORDINATES` in `config.py` contains exact pixel coordinates measured via Android's pointer location developer tool. Used when element selectors fail during scroll operations due to stale element references.

### Stop Condition Logic
The scraper stops when encountering a person with name starting with "Shengli Oilfield" (`scraper.py:56`). This is app-specific and should be updated for different target apps or data sets.

### Database Schema
```sql
CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    scraped_at TIMESTAMP,
    raw_data TEXT  -- JSON: {"all_fields": [...], "field_count": N}
)
```

## Common Tasks

### Adjusting for New Target App
1. Run `setup.py` with new app open
2. Update `APP_PACKAGE` in config.py
3. Inspect `hierarchy.xml` for list structure
4. Update `LIST_ITEM_SELECTOR`, `LIST_CONTAINER_SELECTOR`
5. Update detail page selectors: `SHOW_MORE_BUTTON`, name extraction in extractor.py
6. Adjust scroll logic and stop condition in scraper.py

### Debugging Element Selectors
- Use `inspect_detail.py` to dump current screen hierarchy
- Check `scraper.log` for element not found errors
- View error screenshots in `screenshots/` directory
- Verify selectors exist in dumped XML with exact resourceId/text

### Handling Scroll Issues
- Measure items per screen, update `index == 11` threshold
- Use `get_coordinates.py` to measure precise click coordinates
- Adjust `SCROLL_WAIT` if content loads slowly after scroll

### Performance Optimization
Current config is tuned for **maximum speed**:
- `CLICK_TIMEOUT = 0.2s`
- `PAGE_LOAD_TIMEOUT = 0.8s`
- `SCROLL_WAIT = 0.1s`

Increase timeouts if encountering frequent errors or missed elements.
