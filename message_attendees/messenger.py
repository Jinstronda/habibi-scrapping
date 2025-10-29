"""Message orchestration logic."""
import sys
import os
# Add message_attendees for local config.py
sys.path.insert(0, os.path.dirname(__file__))
# Add scraper_attendees for device.py and utils.py
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import logging
import config
from message_sender import (
    click_search_icon, type_name, click_search_result,
    click_direct_message, type_and_send_message, return_to_main
)
from database import message_already_sent, save_message_record
from utils import take_screenshot

logger = logging.getLogger(__name__)

def message_single_attendee(device, name, message):
    """Send message to single attendee."""
    logger.info(f"Messaging: {name}")
    
    if not click_search_icon(device):
        logger.error(f"Failed to click search icon for {name}")
        return False
    
    if not type_name(device, name):
        logger.error(f"Failed to type name: {name}")
        return False
    
    if not click_search_result(device, name):
        logger.warning(f"Search result not found for: {name}")
        return_to_main(device)
        return False
    
    if not click_direct_message(device):
        logger.warning(f"Direct message not available for: {name}")
        return_to_main(device)
        return False
    
    if not type_and_send_message(device, message):
        logger.error(f"Failed to send message to: {name}")
        if config.SAVE_SCREENSHOTS_ON_ERROR:
            take_screenshot(device, f"error_{name}")
        return_to_main(device)
        return False
    
    logger.info(f"✓ Message sent to {name}")
    return_to_main(device)
    return True

def message_all_attendees(device, attendees, message):
    """Send messages to list of attendees."""
    total = len(attendees)
    sent = 0
    skipped = 0
    failed = 0
    
    logger.info(f"Starting to message {total} attendees")
    
    for i, name in enumerate(attendees, 1):
        logger.info(f"[{i}/{total}] Processing: {name}")
        
        if config.SKIP_ALREADY_MESSAGED and message_already_sent(name):
            logger.info(f"Skipped {name} (already messaged)")
            skipped += 1
            continue
        
        success = message_single_attendee(device, name, message)
        save_message_record(name, message, success)
        
        if success:
            sent += 1
        else:
            failed += 1
    
    logger.info(f"Complete! Sent: {sent}, Skipped: {skipped}, Failed: {failed}")
    return sent

