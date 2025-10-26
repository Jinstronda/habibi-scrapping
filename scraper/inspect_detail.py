"""Inspect detail page to find 'show more' button selector."""
import uiautomator2 as u2
import time
import config

def inspect_detail_page():
    """Click first person and dump detail page hierarchy."""
    print("=== Detail Page Inspector ===\n")
    print("Connecting to device...")
    device = u2.connect(config.DEVICE_SERIAL)

    print(f"Looking for list items with selector: {config.LIST_ITEM_SELECTOR}")
    first_item = device(**config.LIST_ITEM_SELECTOR)[0]

    if not first_item.exists(timeout=3):
        print("\n❌ Error: First list item not found!")
        print("Make sure you're on the Speakers list page")
        return

    print("✓ Found first person in list")
    print("Clicking first person...")
    first_item.click()

    print("Waiting for page to load (checking for ProgressBar)...")
    time.sleep(5)

    loading = device(resourceId="com.swapcard.apps.android.adipec:id/layout_loading")
    if loading.exists(timeout=2):
        print("Page still loading, waiting...")
        time.sleep(3)

    print("Scrolling detail page to reveal all content...")
    pager = device(resourceId="com.swapcard.apps.android.adipec:id/detail_pager_sections")
    if pager.exists(timeout=2):
        for _ in range(3):
            pager.scroll.forward()
            time.sleep(1)

    print("Dumping complete detail page hierarchy...")
    xml = device.dump_hierarchy()

    output_file = "detail_page_hierarchy.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)

    print(f"\n✓ Detail page hierarchy saved to: {output_file}")
    print("\nSearch for 'show more' or 'more' in the file to find the button")
    print("Look for attributes like:")
    print("  - text='...'")
    print("  - resource-id='...'")
    print("  - content-desc='...'")
    print("\nUpdate config.py SHOW_MORE_BUTTON with the correct selector")

    print("\nPress Enter to go back to list...")
    input()
    device.press("back")
    print("✓ Returned to list")

if __name__ == "__main__":
    inspect_detail_page()
