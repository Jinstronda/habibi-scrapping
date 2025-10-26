"""Core scraping logic for attendees list."""
import time
import logging
import config
from extractor import extract_from_list_view, extract_from_detail_page, is_truncated, parse_company_role
from database import attendee_exists, save_attendee
from utils import take_screenshot

logger = logging.getLogger(__name__)

def scrape_single_attendee(device, index):
    """Scrape data from one attendee with fast path."""
    name, company_role = extract_from_list_view(device, index)

    if not name or not company_role:
        return None

    if attendee_exists(name):
        logger.info(f"Skipped {name} (already in database)")
        return "skipped"

    # Fast path: not truncated
    if not is_truncated(company_role):
        company, role = parse_company_role(company_role)
        save_attendee(name, company, role, False)
        logger.info(f"✓ Fast: {name} | {company} - {role}")
        return "saved_fast"

    # Slow path: truncated, need detail page
    try:
        items = device(**config.LIST_ITEM_SELECTOR)
        if index >= items.count:
            return None

        items[index].click()
        time.sleep(config.PAGE_LOAD_TIMEOUT)

        full_company, full_role = extract_from_detail_page(device)
        device.press("back")
        time.sleep(config.CLICK_TIMEOUT)

        # Use extracted values or fallback to parsed text
        company = full_company or parse_company_role(company_role)[0]
        role = full_role or parse_company_role(company_role)[1]

        save_attendee(name, company, role, True)
        logger.info(f"⚡ Detail: {name} | {company} - {role}")
        return "saved_detail"

    except Exception as e:
        logger.error(f"Failed to scrape attendee: {e}")
        if config.SAVE_SCREENSHOTS_ON_ERROR:
            take_screenshot(device, "error")
        device.press("back")
        time.sleep(config.CLICK_TIMEOUT)
        return None

def scrape_all_attendees(device):
    """Main scraping loop for attendees."""
    scraped_count = 0
    fast_count = 0
    detail_count = 0
    swipe_count = 0
    index = 0

    logger.info("Starting attendees scraper")

    while True:
        if config.MAX_ATTENDEES and scraped_count >= config.MAX_ATTENDEES:
            logger.info(f"Reached MAX_ATTENDEES limit: {config.MAX_ATTENDEES}")
            break

        result = scrape_single_attendee(device, index)

        if result == "saved_fast":
            scraped_count += 1
            fast_count += 1
        elif result == "saved_detail":
            scraped_count += 1
            detail_count += 1

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
                    logger.info(f"Scroll complete")
                else:
                    logger.warning("List container not found")
            except Exception as e:
                logger.warning(f"Scroll error: {e}")

    logger.info(f"Complete! Total: {scraped_count} (Fast: {fast_count}, Detail: {detail_count})")
    return scraped_count
