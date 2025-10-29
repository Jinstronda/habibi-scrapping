"""Individual message sending operations."""
import sys
import os
# Add message_attendees for local config.py
sys.path.insert(0, os.path.dirname(__file__))
# Add scraper_attendees for device.py and utils.py
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import time
import logging
import config

logger = logging.getLogger(__name__)

def click_search_icon(device):
    """Click the search icon to open search."""
    search_icon = device(**config.SEARCH_ICON_SELECTOR)
    if search_icon.exists(timeout=2):
        search_icon.click()
        time.sleep(config.CLICK_TIMEOUT)
        return True
    return False

def type_name(device, name):
    """Type attendee name into search field and trigger search."""
    search_input = device(**config.SEARCH_INPUT_SELECTOR)
    if search_input.exists(timeout=1):
        # Clear any existing text first
        search_input.clear_text()
        time.sleep(0.2)
        # Type new name
        search_input.set_text(name)
        logger.info(f"Typed search query: {name}")
        # Press Enter to trigger search
        device.press("enter")
        logger.info("Pressed Enter to trigger search")
        time.sleep(config.SEARCH_WAIT)
        return True
    return False

def click_search_result(device, expected_name):
    """Click search result that matches expected name (checks ALL results)."""
    # Wait a bit more for results to appear
    time.sleep(0.5)
    
    results = device(**config.SEARCH_RESULT_SELECTOR)
    if not results.exists(timeout=3):
        logger.warning("No search results found")
        return False
    
    # Check ALL results (up to 15), not just the first one
    max_results = min(results.count, 15)
    logger.info(f"Found {max_results} search results, checking for '{expected_name}'")
    
    for i in range(max_results):
        result = results[i]
        if result.exists(timeout=0.5):
            # Get text from child TextViews
            text_views = result.child(className="android.widget.TextView")
            texts = []
            for j in range(text_views.count):
                text = text_views[j].get_text()
                if text and text.strip():
                    texts.append(text.strip())
            
            result_name = texts[0] if texts else ""
            logger.debug(f"Result {i}: {result_name}")
            
            if result_name and expected_name.lower() in result_name.lower():
                logger.info(f"✓ Found match at position {i}: {result_name}")
                result.click()
                time.sleep(config.PAGE_LOAD_TIMEOUT)
                return True
    
    logger.warning(f"✗ No match found for '{expected_name}' in {max_results} results")
    return False

def click_direct_message(device):
    """Click direct message button on profile."""
    dm_button = device(**config.DIRECT_MESSAGE_BUTTON)
    if dm_button.exists(timeout=2):
        dm_button.click()
        time.sleep(config.PAGE_LOAD_TIMEOUT)
        return True
    return False

def type_and_send_message(device, message):
    """Type message and send it."""
    msg_input = device(**config.MESSAGE_INPUT_SELECTOR)
    if not msg_input.exists(timeout=1):
        logger.error("Message input field not found")
        return False
    
    # Click on the input field to focus it
    msg_input.click()
    time.sleep(0.3)
    
    # Type the message
    msg_input.set_text(message)
    logger.info(f"Typed message: {message}")
    time.sleep(0.5)
    
    # Click the SEND button
    send_btn = device(**config.SEND_BUTTON_SELECTOR)
    if not send_btn.exists(timeout=2):
        logger.error("SEND button not found")
        return False
    
    logger.info("Clicking SEND button")
    send_btn.click()
    logger.info("Waiting 1 second for message to send...")
    time.sleep(1.0)
    
    logger.info("Message sent successfully")
    return True

def return_to_main(device):
    """Press back 2 times to return to search screen and clear search field."""
    for _ in range(2):
        device.press("back")
        time.sleep(config.CLICK_TIMEOUT)
    
    # Clear search field if it has old text
    time.sleep(0.5)
    search_input = device(**config.SEARCH_INPUT_SELECTOR)
    if search_input.exists(timeout=1):
        search_input.clear_text()
        time.sleep(0.2)

