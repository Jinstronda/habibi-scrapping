"""Test script to send a single message to verify all selectors work."""
import sys
import os
# Add message_attendees directory FIRST so local config.py is found
sys.path.insert(0, os.path.dirname(__file__))
# Then add scraper_attendees for device and utils
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

from device import connect_device
from message_sender import (
    click_search_icon, type_name, click_search_result,
    click_direct_message, type_and_send_message, return_to_main
)

def test_send_message():
    """Test sending a message to Aaron Yap."""
    print("=== Testing Message Bot ===\n")
    
    device = connect_device()
    test_name = "Aaron Yap"
    test_message = "Looking forward to the event"
    
    print(f"Target: {test_name}")
    print(f"Message: {test_message}\n")
    
    # Step 1: Click search icon
    print("Step 1: Clicking search icon...")
    if not click_search_icon(device):
        print("❌ Failed to click search icon")
        return
    print("✓ Search icon clicked\n")
    
    # Step 2: Type name
    print(f"Step 2: Typing '{test_name}'...")
    if not type_name(device, test_name):
        print("❌ Failed to type name")
        return
    print("✓ Name typed\n")
    
    # Step 3: Click search result
    print("Step 3: Clicking search result...")
    if not click_search_result(device, test_name):
        print("❌ Search result not found")
        return
    print("✓ Profile opened\n")
    
    # Step 4: Click Direct Message
    print("Step 4: Clicking Direct Message button...")
    if not click_direct_message(device):
        print("❌ Direct Message button not found")
        return
    print("✓ Message screen opened\n")
    
    # Step 5: Type and send message
    print(f"Step 5: Typing and sending message...")
    if not type_and_send_message(device, test_message):
        print("❌ Failed to send message")
        return
    print("✓ Message sent!\n")
    
    # Step 6: Return to main
    print("Step 6: Returning to main screen...")
    return_to_main(device)
    print("✓ Returned to search\n")
    
    print("=" * 50)
    print("✅ SUCCESS! Message bot is working correctly!")
    print("=" * 50)
    print("\nReady to run: python main.py")

if __name__ == "__main__":
    test_send_message()

