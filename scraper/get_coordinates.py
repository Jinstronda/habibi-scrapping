"""Get screen coordinates for list items."""
import sys
sys.path.insert(0, 'C:\\Users\\joaop\\Documents\\Augusta Labs\\Scrapper for Gui\\scraper')
import uiautomator2 as u2
import config
import xml.etree.ElementTree as ET

device = u2.connect(config.DEVICE_SERIAL)
print(f"Connected to device")

# Dump hierarchy and find ALL items with content_layout
xml = device.dump_hierarchy()
root = ET.fromstring(xml)

print("\nSearching for all elements with content_layout resourceId...")
items_found = []

for elem in root.iter():
    res_id = elem.get('resource-id')
    if res_id and 'content_layout' in res_id:
        bounds_str = elem.get('bounds')
        if bounds_str:
            # Parse bounds: [left,top][right,bottom]
            import re
            match = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
            if match:
                left, top, right, bottom = map(int, match[0])
                x = (left + right) // 2
                y = (top + bottom) // 2
                items_found.append((x, y, bounds_str))

print(f"\nFound {len(items_found)} items total:")
for i, (x, y, bounds) in enumerate(items_found):
    print(f"Item {i}: ({x}, {y}) - {bounds}")

print(f"\nPython list format:")
coords = [(x, y) for x, y, _ in items_found]
print(f"ITEM_COORDINATES = {coords}")
