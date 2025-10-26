"""Utility functions for scraper."""
import logging
import time
from functools import wraps
from datetime import datetime
import config

def setup_logging():
    """Configure logging for scraper."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def retry_on_failure(max_attempts=3, delay=1):
    """Retry decorator for flaky operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

def take_screenshot(device, name):
    """Save screenshot for debugging."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{config.SCREENSHOT_DIR}/{name}_{timestamp}.png"
    device.screenshot(filename)
    return filename
