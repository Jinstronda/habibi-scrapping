"""Automatically navigate messaging flow and dump XML files."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import uiautomator2 as u2
import time

def discover_selectors():
    """Auto-navigate through messaging and dump XMLs."""
    print("=== Auto Selector Discovery ===\n")
    device = u2.connect()
    
    # STEP 1: Click search icon
    print("STEP 1: Clicking search icon...")
    search_icon = device(resourceId="com.swapcard.apps.android.adipec:id/action_search")
    if search_icon.exists(timeout=3):
        search_icon.click()
        time.sleep(1)
        
        xml = device.dump_hierarchy()
        with open("search_screen.xml", "w", encoding="utf-8") as f:
            f.write(xml)
        print("✓ Saved search_screen.xml\n")
    else:
        print("✗ Search icon not found!\n")
        return
    
    # STEP 2: Type a test name from test_list.txt
    print("STEP 2: Typing 'Aaron Yap'...")
    search_input = device(resourceId="com.swapcard.apps.android.adipec:id/search_src_text")
    if search_input.exists(timeout=2):
        search_input.set_text("Aaron Yap")
        time.sleep(1.5)  # Wait for search results
        
        xml = device.dump_hierarchy()
        with open("search_results.xml", "w", encoding="utf-8") as f:
            f.write(xml)
        print("✓ Saved search_results.xml\n")
    else:
        print("✗ Search input not found!\n")
        return
    
    # STEP 3: Click first result
    print("STEP 3: Clicking first search result...")
    results = device(resourceId="com.swapcard.apps.android.adipec:id/content_layout")
    if results.exists(timeout=2):
        results[0].click()
        time.sleep(2)  # Wait for profile to load
        
        xml = device.dump_hierarchy()
        with open("profile_screen.xml", "w", encoding="utf-8") as f:
            f.write(xml)
        print("✓ Saved profile_screen.xml\n")
    else:
        print("✗ Search results not found!\n")
        return
    
    print("\nDONE! Files saved:")
    print("  - search_screen.xml")
    print("  - search_results.xml")
    print("  - profile_screen.xml")
    print("\nNow manually click 'Direct message' and run:")
    print("  python dump_message_screen.py")

if __name__ == "__main__":
    discover_selectors()

