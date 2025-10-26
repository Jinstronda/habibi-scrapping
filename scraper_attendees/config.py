"""Configuration for Android attendees scraper."""

# Device settings
DEVICE_SERIAL = None  # None = auto-detect first device
SCREENSHOT_DIR = "screenshots_attendees"

# Timeouts (seconds) - MAXIMUM SPEED
CLICK_TIMEOUT = 0.2
PAGE_LOAD_TIMEOUT = 0.8
SCROLL_WAIT = 0.1

# Element selectors - UPDATE THESE after UI inspection with setup.py
APP_PACKAGE = "com.swapcard.apps.android.adipec"
LIST_CONTAINER_SELECTOR = {"resourceId": "android:id/list"}

# List item container - each attendee row
LIST_ITEM_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/content_layout"}

# NOTE: Extractor extracts directly from XML hierarchy
# List view structure (visible in screenshots):
#   - Name: bold text (e.g., "Ally Zhu", "Joy Zhu")
#   - Company-Role: gray text below name (e.g., "Xecta - Senior Petroleum Engineer")
# Detail view structure (when clicked):
#   - "Company Name" label followed by full company
#   - "Job Title" label followed by full role

# Item coordinates (EXACT - user measured with pointer location)
ITEM_COORDINATES = [
    (498, 374),    # Item 0
    (498, 640),    # Item 1
    (498, 929),    # Item 2
    (498, 1011),   # Item 3
    (498, 1190),   # Item 4
    (498, 1374),   # Item 5
    (498, 1558),   # Item 6
    (498, 1732),   # Item 7
    (498, 1895),   # Item 8
    (498, 2108),   # Item 9
    (498, 2217),   # Item 10
]

# Database
DB_PATH = "attendees_data.db"

# Scraping behavior
MAX_RETRIES = 3
SAVE_SCREENSHOTS_ON_ERROR = True
MAX_ATTENDEES = None  # None = unlimited, or set a number for fixed count
