"""Data extraction for attendees list."""
import time
import logging
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
            logger.debug(f"Index {index}: {texts[0]} | {texts[1]}")
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
