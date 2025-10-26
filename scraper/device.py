"""Device connection and management."""
import uiautomator2 as u2
import config

def connect_device():
    """Connect to Android emulator/device."""
    device = u2.connect(config.DEVICE_SERIAL)
    device.implicitly_wait(config.CLICK_TIMEOUT)
    return device

def get_device_info(device):
    """Get device information."""
    return {
        "model": device.device_info.get("model"),
        "version": device.device_info.get("version"),
        "serial": device.serial
    }

def is_app_running(device, package_name):
    """Check if app is currently running."""
    return device.app_current().get("package") == package_name
