"""Main entry point for message attendees bot."""
import sys
import os
# Add message_attendees for local config.py
sys.path.insert(0, os.path.dirname(__file__))
# Add scraper_attendees for device.py and utils.py
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import config
from utils import setup_logging
from device import connect_device, get_device_info
from database import init_messages_db, get_attendees_to_message, get_message_stats
from messenger import message_all_attendees

def main():
    """Run the message attendees bot."""
    logger = setup_logging()
    logger.info("Starting message attendees bot")
    
    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    init_messages_db()
    
    device = connect_device()
    logger.info(f"Connected to device: {get_device_info(device)}")
    
    if not config.APP_PACKAGE:
        logger.error("APP_PACKAGE not set in config.py")
        return
    
    attendees = get_attendees_to_message()
    if not attendees:
        logger.error("No attendees found. Check config.py settings.")
        return
    
    source = "test_list.txt" if config.USE_TEST_LIST else "database"
    logger.info(f"Loaded {len(attendees)} attendees from {source}")
    
    total_sent = message_all_attendees(device, attendees, config.DEFAULT_MESSAGE)
    
    total_msgs, successful = get_message_stats()
    logger.info(f"Session complete! Sent: {total_sent}")
    logger.info(f"Total messages in history: {total_msgs} ({successful} successful)")

if __name__ == "__main__":
    main()

