"""Data extraction for attendees list."""
import time
import logging
import re
import config
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def is_truncated(text):
    """Check if company-role text is truncated."""
    return text.strip().endswith('...')

def parse_company_role(company_role_text):
    """Parse 'Company - Role' format into separate fields."""
    if ' - ' in company_role_text:
        parts = company_role_text.split(' - ', 1)
        return parts[0].strip(), parts[1].strip()
    return company_role_text.strip(), ""

def extract_from_list_view(device, index):
    """Extract name and company-role text from list view."""
    try:
        items = device(**config.LIST_ITEM_SELECTOR)
        if index >= items.count:
            return None, None

        item = items[index]
        if not item.exists(timeout=0.3):
            return None, None

        # Get text directly from child elements using uiautomator2
        # Find all TextViews within this specific list item
        text_views = item.child(className="android.widget.TextView")

        texts = []
        for i in range(text_views.count):
            text = text_views[i].get_text()
            if text and text.strip():
                texts.append(text.strip())

        # First text is name, second is company-role
        if len(texts) >= 2:
            return texts[0], texts[1]

        return None, None
    except Exception as e:
        logger.debug(f"Extract error at index {index}: {e}")
        return None, None

def extract_from_detail_page(device):
    """Extract full company name and job title from detail page."""
    time.sleep(config.PAGE_LOAD_TIMEOUT)

    xml = device.dump_hierarchy()
    root = ET.fromstring(xml)

    company = None
    job_title = None
    found_company_label = False
    found_job_title_label = False

    # Find "Company Name" and "Job Title" labels, then get next text
    for elem in root.iter():
        text = elem.get('text', '').strip()

        if text == 'Company Name':
            found_company_label = True
        elif found_company_label and text and company is None:
            company = text
            found_company_label = False

        if text == 'Job Title':
            found_job_title_label = True
        elif found_job_title_label and text and job_title is None:
            job_title = text
            found_job_title_label = False

    return company, job_title

# ===== BATCH EXTRACTION (EXPERIMENTAL) =====

def _parse_bounds(bounds_input):
    """Parse bounds from dict or string."""
    if not bounds_input:
        return None

    # Handle dict format from item.info
    if isinstance(bounds_input, dict):
        return (bounds_input.get('left', 0), bounds_input.get('top', 0),
                bounds_input.get('right', 0), bounds_input.get('bottom', 0))

    # Handle string format '[0,374][1080,640]'
    if isinstance(bounds_input, str):
        match = re.findall(r'\[(\d+),(\d+)\]', bounds_input)
        if len(match) == 2:
            left, top = int(match[0][0]), int(match[0][1])
            right, bottom = int(match[1][0]), int(match[1][1])
            return (left, top, right, bottom)

    return None

def _is_within_bounds(elem_bounds, parent_bounds):
    """Check if element bounds are within parent bounds."""
    if not elem_bounds or not parent_bounds:
        return False
    e_left, e_top, e_right, e_bottom = elem_bounds
    p_left, p_top, p_right, p_bottom = parent_bounds
    return (e_left >= p_left and e_top >= p_top and
            e_right <= p_right and e_bottom <= p_bottom)

def _extract_texts_from_item(xml_root, item_bounds):
    """Extract TextView texts within item bounds."""
    texts = []
    for elem in xml_root.iter():
        if elem.get('class') == 'android.widget.TextView':
            elem_bounds_str = elem.get('bounds', '')
            elem_bounds = _parse_bounds(elem_bounds_str)
            if _is_within_bounds(elem_bounds, item_bounds):
                text = elem.get('text', '').strip()
                if text:
                    texts.append(text)
    return texts

def extract_batch_from_list_view(device, count=11):
    """Extract multiple items from single XML dump (FAST)."""
    try:
        # Get item references
        items = device(**config.LIST_ITEM_SELECTOR)
        actual_count = min(count, items.count)

        # Get all item bounds first
        item_bounds_list = []
        for i in range(actual_count):
            item = items[i]
            if item.exists(timeout=0.1):
                bounds_str = item.info.get('bounds')
                bounds = _parse_bounds(bounds_str)
                if bounds:
                    item_bounds_list.append((i, bounds))

        # Single XML dump for all items
        xml = device.dump_hierarchy()
        root = ET.fromstring(xml)

        # Extract from XML locally (no more device calls!)
        results = {}
        for index, bounds in item_bounds_list:
            texts = _extract_texts_from_item(root, bounds)
            if len(texts) >= 2:
                results[index] = (texts[0], texts[1])

        return results
    except Exception as e:
        logger.error(f"Batch extraction error: {e}")
        return {}
