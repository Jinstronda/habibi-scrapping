"""Configuration for message attendees bot."""

# Device settings
DEVICE_SERIAL = None  # None = auto-detect first device

# Timeouts (seconds)
CLICK_TIMEOUT = 0.3
PAGE_LOAD_TIMEOUT = 1.0
SEARCH_WAIT = 2.0  # Wait for search results to load (increased for network delay)
MESSAGE_SENT_WAIT = 1.0  # Wait after sending message

# App package
APP_PACKAGE = "com.swapcard.apps.android.adipec"

# Element selectors - ✅ FULLY CONFIGURED from XML dumps

# STEP 1: Click search icon (found from hierarchy.xml)
SEARCH_ICON_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/action_search"}

# STEP 2: Type in search field (found in search_screen.xml)
SEARCH_INPUT_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/search_src_text"}

# STEP 3: Click search result (found from hierarchy.xml)
SEARCH_RESULT_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/content_layout"}

# STEP 4: Click Direct Message button (found in profile_screen.xml)
DIRECT_MESSAGE_BUTTON = {"description": "Direct Message"}  # content-desc

# STEP 5: Type message (found in message_screen.xml)
MESSAGE_INPUT_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/edit_text_message"}

# STEP 6: Send message (found in message_screen.xml)
SEND_BUTTON_SELECTOR = {"resourceId": "com.swapcard.apps.android.adipec:id/btn_send"}

# Message template
DEFAULT_MESSAGE = "Hey, looking forward to meeting you at the event!"

# Data sources (relative to this config file's directory)
import os as _os
_CONFIG_DIR = _os.path.dirname(_os.path.abspath(__file__))
TEST_LIST_FILE = _os.path.join(_CONFIG_DIR, "test_list.txt")
ATTENDEES_DB_PATH = _os.path.join(_CONFIG_DIR, "..", "scraper_attendees", "attendees_data.db")
MESSAGES_DB_PATH = _os.path.join(_CONFIG_DIR, "messages_data.db")
SCREENSHOT_DIR = _os.path.join(_CONFIG_DIR, "screenshots_messages")

# Behavior
MAX_RETRIES = 2
SAVE_SCREENSHOTS_ON_ERROR = True
USE_TEST_LIST = True  # False = use full database
SKIP_ALREADY_MESSAGED = True  # Check messages DB before sending

