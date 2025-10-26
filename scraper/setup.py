"""Setup script to identify app package and inspect UI."""
import uiautomator2 as u2
import subprocess

def find_package_name():
    """List all packages and help identify target app."""
    try:
        print("Fetching installed packages from emulator...")
        result = subprocess.run(
            ["adb", "shell", "pm", "list", "packages"],
            capture_output=True,
            text=True,
            check=True
        )
        packages = sorted([p.replace("package:", "") for p in result.stdout.strip().split("\n")])
        print(f"\nFound {len(packages)} packages.")
        print("\nLast 20 packages (likely user-installed apps):")
        for pkg in packages[-20:]:
            print(f"  {pkg}")
        return packages
    except (FileNotFoundError, subprocess.SubprocessError):
        print("\n(adb not found in PATH - skipping package list)")
        return []

def inspect_current_app():
    """Inspect currently open app."""
    device = u2.connect()
    current = device.app_current()
    print(f"\nCurrently running app:")
    print(f"  Package: {current['package']}")
    print(f"  Activity: {current['activity']}")

    print("\nDumping UI hierarchy...")
    xml = device.dump_hierarchy()
    print(f"UI hierarchy saved to: hierarchy.xml")
    with open("hierarchy.xml", "w", encoding="utf-8") as f:
        f.write(xml)

    return current['package']

def main():
    """Run setup to identify app and UI elements."""
    print("=== Android App Scraper Setup ===\n")
    print("Step 1: Make sure your emulator is running")
    print("Step 2: Open the target app on the emulator")
    input("\nPress Enter when ready...")

    package = inspect_current_app()
    find_package_name()

    print(f"\n✓ Update config.py with: APP_PACKAGE = '{package}'")
    print("✓ Open hierarchy.xml to find element selectors")
    print("✓ Update LIST_ITEM_SELECTOR in config.py")

if __name__ == "__main__":
    main()
