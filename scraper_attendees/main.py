"""Main entry point for Android attendees scraper."""
import os
import config
from utils import setup_logging
from device import connect_device, get_device_info
from database import init_db
from scraper import scrape_all_attendees

def main():
    """Run the attendees scraper."""
    logger = setup_logging()
    logger.info("Starting Android attendees scraper")

    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    init_db()

    device = connect_device()
    logger.info(f"Connected to device: {get_device_info(device)}")

    if not config.APP_PACKAGE:
        logger.error("APP_PACKAGE not set in config.py. Run setup.py first.")
        return

    total_scraped = scrape_all_attendees(device)
    logger.info(f"Scraping complete! Total attendees scraped: {total_scraped}")

if __name__ == "__main__":
    main()
