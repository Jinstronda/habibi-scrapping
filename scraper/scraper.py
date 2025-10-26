"""Core scraping logic for iterating through list."""
import time
import logging
import config
from extractor import extract_person_data
from database import person_exists, save_person
from utils import take_screenshot

logger = logging.getLogger(__name__)

def scrape_single_person(device, index):
    """Scrape data from one person using element recognition."""
    try:
        # Get fresh element reference each time
        items = device(**config.LIST_ITEM_SELECTOR)
        if index >= items.count:
            return None

        item = items[index]
        if not item.exists(timeout=0.3):
            return None

        item.click()
        time.sleep(config.PAGE_LOAD_TIMEOUT)
    except Exception as e:
        logger.debug(f"Click failed at index {index}: {e}")
        return None

    try:
        name, data = extract_person_data(device)
        device.press("back")
        time.sleep(config.CLICK_TIMEOUT)
        return name, data
    except Exception as e:
        logger.error(f"Failed to scrape person: {e}")
        if config.SAVE_SCREENSHOTS_ON_ERROR:
            take_screenshot(device, "error")
        device.press("back")
        time.sleep(config.CLICK_TIMEOUT)
        return None

def scrape_all_people(device):
    """Main scraping loop."""
    scraped_count = 0
    swipe_count = 0
    index = 0

    logger.info("Starting scraper from current position")

    while True:
        result = scrape_single_person(device, index)
        if result:
            name, data = result

            # ONLY stop condition: reached end marker
            if name.startswith("Shengli Oilfield"):
                logger.info(f"Stopping - reached end of list marker: '{name}'")
                break

            if not person_exists(name):
                save_person(name, data)
                scraped_count += 1
                logger.info(f"Scraped {name} ({scraped_count} total)")
            else:
                logger.info(f"Skipped {name} (already in database)")

        index += 1

        if index == 11:
            swipe_count += 1
            logger.info(f"Scrolling (swipe #{swipe_count})")
            try:
                list_container = device(**config.LIST_CONTAINER_SELECTOR)
                if list_container.exists(timeout=0.5):
                    list_container.scroll.backward()
                    time.sleep(0.3)
                    index = 0
                    logger.info(f"Scroll complete (swipe {swipe_count})")
                else:
                    logger.warning("List container not found")
            except Exception as e:
                logger.warning(f"Scroll error: {e}")

    logger.info(f"Complete! Total swipes: {swipe_count}, saved {scraped_count} new people")
    return scraped_count
