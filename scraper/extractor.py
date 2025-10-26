"""Data extraction from detail pages."""
import time
import logging
import config
from utils import retry_on_failure

logger = logging.getLogger(__name__)

def click_show_more(device):
    """Click 'show more' button to expand details."""
    button = device(**config.SHOW_MORE_BUTTON)
    if button.exists(timeout=0.3):
        button.click()
        logger.info("Clicked 'show more' button")
        return True
    return False

def scroll_detail_page(device):
    """Scroll detail page to reveal all expanded content."""
    pager = device(resourceId="com.swapcard.apps.android.adipec:id/detail_pager_sections")
    if pager.exists(timeout=0.3):
        pager.scroll.forward()
        time.sleep(0.1)
        return True
    return False

def extract_all_text(device):
    """Extract all visible text from current page."""
    xml = device.dump_hierarchy()
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml)
    texts = []
    for elem in root.iter():
        text = elem.get('text')
        if text and text.strip():
            texts.append(text.strip())
    return texts

def extract_person_name(device):
    """Extract person's name from detail page header."""
    name_elem = device(resourceId="com.swapcard.apps.android.adipec:id/header_name")
    if name_elem.exists(timeout=0.5):
        return name_elem.get_text()
    return "Unknown"

def extract_person_data(device):
    """Extract all data from person detail page."""
    name = extract_person_name(device)

    clicked = click_show_more(device)
    if clicked:
        scroll_detail_page(device)

    all_text = extract_all_text(device)
    data = {
        "all_fields": all_text,
        "field_count": len(all_text)
    }
    return name, data
