# Message Attendees Bot

Automates sending direct messages to event attendees through the ADIPEC app.

## The Problem

You have a list of attendees to message. Doing it manually:
1. Click search
2. Type name
3. Click person
4. Click "Direct message"
5. Type message
6. Send
7. Press back 3 times
8. Repeat 100 times

This takes forever.

## The Solution

This bot does it automatically. Give it a list of names, it messages everyone.

**Speed:** ~10 seconds per person (including navigation)

## Setup

### 1. Prerequisites

- Python with conda environment `turing0.1`
- Android emulator running
- ADIPEC app installed and logged in
- ADB working

```bash
conda activate turing0.1
cd message_attendees
pip install -r requirements.txt
```

### 2. Discover UI Elements

Open the app to the Attendees tab (where you can see the search bar).

```bash
python setup.py
```

This dumps the UI to `hierarchy.xml`. Open it and find:
- Search bar selector
- Search result item selector  
- "Direct message" button
- Message input field
- Send button

Update `config.py` with the correct selectors.

### 3. Prepare Your List

Edit `test_list.txt` with attendee names (one per line):
```
John Smith
Jane Doe
Bob Johnson
```

Or set `USE_TEST_LIST = False` in config.py to message everyone from the scraper database.

## Run It

```bash
python main.py
```

It will:
1. Read attendees from test_list.txt (or database)
2. For each person:
   - Search their name
   - Click profile
   - Click "Direct message"
   - Send message
   - Return to search
3. Track sent messages (won't duplicate)

## Configuration

Edit `config.py`:

```python
# Message template
DEFAULT_MESSAGE = "Looking forward to the event"

# Data source
USE_TEST_LIST = True  # False = use full scraper database

# Behavior
SKIP_ALREADY_MESSAGED = True  # Skip people already messaged
```

## Safety Features

**Duplicate Prevention:** Tracks sent messages in `messages_data.db`. Won't message the same person twice.

**Error Handling:** If search fails or direct message unavailable, skips person and continues.

**Screenshots:** Saves screenshots on errors for debugging.

## Output

Database: `messages_data.db`

Tracks:
- Attendee name
- Message sent
- Timestamp
- Success/failure

Check progress:
```python
import sqlite3
conn = sqlite3.connect('messages_data.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM messages")
for row in cursor.fetchall():
    print(row)
```

## Workflow

### Testing (Recommended First)

1. Add 5 names to `test_list.txt`
2. Set `USE_TEST_LIST = True` in config.py
3. Run `python main.py`
4. Verify messages sent correctly

### Production

1. Set `USE_TEST_LIST = False` in config.py
2. Run `python main.py`
3. Let it run (can take hours for large lists)
4. Press Ctrl+C to stop (safe, tracks progress)
5. Re-run later to continue (skips already messaged)

## Files

```
main.py              # Entry point
config.py            # Settings, selectors, message template
messenger.py         # Orchestration logic
message_sender.py    # Individual message operations
database.py          # Message tracking, attendee reading
device.py            # Device connection (reuses scraper_attendees)
utils.py             # Logging, screenshots (reuses scraper_attendees)
setup.py             # UI element discovery
test_list.txt        # Test attendee names
```

## Troubleshooting

**Search not finding people:**
- Verify SEARCH_BAR_SELECTOR in config.py
- Check if search bar needs clicking first
- Name might be slightly different in app

**Direct message button not found:**
- Update DIRECT_MESSAGE_BUTTON selector in config.py
- Person might not be messageable (not connected)
- Check if button text is different

**Messages not sending:**
- Verify MESSAGE_INPUT_SELECTOR in config.py
- Check SEND_BUTTON_SELECTOR
- Increase MESSAGE_SENT_WAIT timeout

**Back navigation doesn't return to search:**
- Increase CLICK_TIMEOUT in config.py
- May need more than 3 backs (update return_to_main function)

