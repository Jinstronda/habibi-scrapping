# Batch Extraction Mode - Usage Guide

## What is Batch Mode?

**Normal mode:** 7 device calls per attendee = 77 calls per screen (SLOW)
**Batch mode:** 1 XML dump per screen = 1 call per screen (FAST)

**Expected speedup: 50% faster**

---

## How to Enable

### 1. Test it first (recommended)

```bash
cd scraper_attendees
python test_batch.py
```

**Check output:** First 5 names should be IDENTICAL in both NORMAL and BATCH sections.

If they match → batch works! ✓

---

### 2. Enable in config.py

Edit `scraper_attendees/config.py`:

```python
# Change this line from False to True:
USE_BATCH_EXTRACTION = True
```

Save the file.

---

### 3. Run the scraper

```bash
python main.py
```

**Look for:** `Starting attendees scraper (BATCH mode)`

If you see that, batch mode is active!

---

## How to Disable

Edit `config.py`:

```python
USE_BATCH_EXTRACTION = False  # Back to normal mode
```

---

## Troubleshooting

**If extraction fails or gets wrong names:**
- Set `USE_BATCH_EXTRACTION = False` in config.py
- Goes back to normal (slower but proven) mode

**If it works:**
- Enjoy 50% speed boost!
- 1000 attendees: saves ~2.5 minutes

---

## Technical Note

Batch mode only works for **non-truncated** attendees (fast path).

If role text ends with "...", scraper still clicks for details (same as before).

Expected: ~90% of attendees use batch, ~10% still click.
