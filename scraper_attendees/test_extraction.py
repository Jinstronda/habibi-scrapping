"""Test script to verify extraction is working correctly."""
import config
from device import connect_device
from extractor import extract_from_list_view

def test_extraction():
    """Test extracting first 5 attendees from list."""
    print("Connecting to device...")
    device = connect_device()

    print(f"\nApp package: {config.APP_PACKAGE}")
    print(f"List item selector: {config.LIST_ITEM_SELECTOR}")

    print("\nTesting extraction of first 5 list items:\n")
    print("=" * 60)

    for i in range(5):
        name, company_role = extract_from_list_view(device, i)

        if name and company_role:
            print(f"\n[{i}] Name: {name}")
            print(f"    Company-Role: {company_role}")
            print(f"    Truncated: {'YES' if company_role.endswith('...') else 'NO'}")
        else:
            print(f"\n[{i}] ERROR: Could not extract data")

    print("\n" + "=" * 60)
    print("\nIf you see different names for each index, extraction is working!")
    print("If you see the SAME name repeated, there's still a bug.")

if __name__ == "__main__":
    test_extraction()
