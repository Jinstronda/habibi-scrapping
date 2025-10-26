"""Track scraping progress."""
import json
import os

PROGRESS_FILE = "scraper_progress.json"

def save_progress(swipe_count, total_scraped):
    """Save current progress."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({
            'swipe_count': swipe_count,
            'total_scraped': total_scraped
        }, f)

def load_progress():
    """Load saved progress, or start fresh."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            data = json.load(f)
            return data['swipe_count'], data['total_scraped']
    return 0, 0

def reset_progress():
    """Clear progress file."""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
