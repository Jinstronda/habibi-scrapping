"""Setup script to identify UI elements for messaging."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import uiautomator2 as u2

def inspect_current_screen():
    """Inspect currently open screen."""
    device = u2.connect()
    current = device.app_current()
    print(f"\nCurrently running app:")
    print(f"  Package: {current['package']}")
    print(f"  Activity: {current['activity']}")

    print("\nDumping UI hierarchy...")
    xml = device.dump_hierarchy()
    output_file = "hierarchy.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"UI hierarchy saved to: {output_file}")
    return current['package']

def main():
    """Run setup to identify UI elements."""
    print("=== Message Attendees Setup ===\n")
    print("INSTRUCTIONS:")
    print("1. Make sure emulator is running")
    print("2. Open the ADIPEC app")
    print("3. Navigate to the Attendees tab")
    print("4. Make sure you can see the search bar at the top")
    input("\nPress Enter when ready...")

    package = inspect_current_screen()
    
    print(f"\n✓ UI hierarchy dumped to hierarchy.xml")
    print("\nNEXT STEPS:")
    print("1. Open hierarchy.xml")
    print("2. Find these elements and update config.py:")
    print("   - Search bar (input field)")
    print("   - Search result items")
    print("   - Direct message button")
    print("   - Message input field")
    print("   - Send button")

if __name__ == "__main__":
    main()

