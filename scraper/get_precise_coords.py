"""Get PRECISE coordinates by analyzing screen hierarchy."""
import sys
sys.path.insert(0, 'C:\\Users\\joaop\\Documents\\Augusta Labs\\Scrapper for Gui\\scraper')
import uiautomator2 as u2
import config
import xml.etree.ElementTree as ET
import re

device = u2.connect(config.DEVICE_SERIAL)

# Get screen size
width, height = device.window_size()
print(f"Screen size: {width}x{height}")

# Dump hierarchy
xml = device.dump_hierarchy()
root = ET.fromstring(xml)

# Find all items with exact bounds
items = []
for elem in root.iter():
    res_id = elem.get('resource-id')
    if res_id and 'content_layout' in res_id:
        bounds_str = elem.get('bounds')
        if bounds_str:
            match = re.findall(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
            if match:
                left, top, right, bottom = map(int, match[0])
                center_x = (left + right) // 2
                center_y = (top + bottom) // 2
                items.append({
                    'left': left, 'top': top, 'right': right, 'bottom': bottom,
                    'center_x': center_x, 'center_y': center_y,
                    'height': bottom - top
                })

# Sort by Y position
items.sort(key=lambda x: x['top'])

print(f"\nFound {len(items)} items on screen\n")
print("Detailed item positions:")
print("-" * 80)

for i, item in enumerate(items):
    print(f"Item {i}:")
    print(f"  Bounds: [{item['left']},{item['top']}][{item['right']},{item['bottom']}]")
    print(f"  Center: ({item['center_x']}, {item['center_y']})")
    print(f"  Height: {item['height']}px")
    if i > 0:
        gap = item['top'] - items[i-1]['bottom']
        print(f"  Gap from previous: {gap}px")
    print()

print("\nPython config format:")
print("ITEM_COORDINATES = [")
for i, item in enumerate(items):
    print(f"    ({item['center_x']}, {item['center_y']}),  # Item {i}")
print("]")

print(f"\nNote: Screen is {height}px tall, last item center is at Y={items[-1]['center_y']}")
