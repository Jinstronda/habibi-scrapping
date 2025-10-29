"""Dump message screen after you've opened it."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scraper_attendees'))

import uiautomator2 as u2

print("Connecting to device...")
device = u2.connect()

print("Dumping current screen (should be message screen)...")
xml = device.dump_hierarchy()

with open("message_screen.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print("✓ Saved message_screen.xml")
print("\nSearching for message-related elements...")

# Quick analysis
if "message" in xml.lower():
    print("✓ Found 'message' in XML")
if "send" in xml.lower():
    print("✓ Found 'send' in XML")
if "EditText" in xml:
    print("✓ Found EditText (input field)")

print("\nOpen message_screen.xml to find:")
print("  - Message input field (EditText)")
print("  - Send button")

