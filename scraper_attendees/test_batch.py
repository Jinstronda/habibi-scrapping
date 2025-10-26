"""Quick test: Compare batch vs normal extraction."""
import config
from device import connect_device
from extractor import extract_from_list_view, extract_batch_from_list_view

print("Connecting to device...")
device = connect_device()

print("\n=== Testing first 5 items ===\n")

# Normal extraction
print("NORMAL extraction:")
for i in range(5):
    name, company = extract_from_list_view(device, i)
    print(f"  [{i}] {name}")

# Batch extraction
print("\nBATCH extraction:")
batch = extract_batch_from_list_view(device, count=11)
for i in range(5):
    if i in batch:
        name, company = batch[i]
        print(f"  [{i}] {name}")

print("\n✓ If names match above, batch extraction works!")
