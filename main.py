from backend.live_registry.system_info import SystemInfoReader
from backend.live_registry.installed_software import InstalledSoftwareReader
from backend.live_registry.startup_programs import StartupProgramsReader
from backend.live_registry.usb_devices import USBDevicesReader
from backend.live_registry.user_activity import UserActivityReader
def print_system_info():
    """
    Print system information in readable format.
    """
    reader = SystemInfoReader()
    data = reader.get_system_info()

    print("=" * 70)
    print("Portable Windows Registry Forensic Analyzer")
    print("Mode: Live Registry Analysis")
    print("=" * 70)

    print("\nAdministrator Status:")
    print("Running as Admin :", data["admin_status"])

    print("\nComputer Information:")
    print("Computer Name    :", data["computer_name"])
    print("Architecture     :", data["architecture"])
    print("Machine          :", data["machine"])
    print("Processor        :", data["processor"])

    print("\nWindows Information:")
    windows = data["windows_info"]
    print("Product Name     :", windows["product_name"])
    print("Display Version  :", windows["display_version"])
    print("Build Number     :", windows["current_build"])
    print("UBR              :", windows["ubr"])
    print("Edition ID       :", windows["edition_id"])
    print("Install Date     :", windows["install_date"])
    print("System Root      :", windows["system_root"])

    print("\nCurrent User Information:")
    user = data["user_info"]
    print("Username         :", user["username"])
    print("User Domain      :", user["user_domain"])
    print("User Profile     :", user["user_profile"])

    print("\nTimezone Information:")
    timezone = data["timezone_info"]
    print("Time Zone        :", timezone["time_zone"])
    print("Standard Name    :", timezone["standard_name"])

    print("\nSystem info scan completed successfully.")


def print_installed_software():
    """
    Print installed software list in readable format.
    """
    reader = InstalledSoftwareReader()
    data = reader.get_installed_software()

    print("=" * 70)
    print("Installed Software Scan")
    print("=" * 70)

    print("Total Programs Found:", data["total_programs"])
    print("-" * 70)

    for index, software in enumerate(data["software_list"], start=1):
        print(f"\nProgram #{index}")
        print("Name             :", software["name"])
        print("Version          :", software["version"])
        print("Publisher        :", software["publisher"])
        print("Install Date     :", software["install_date"])
        print("Install Location :", software["install_location"])
        print("Registry View    :", software["registry_view"])
        print("Registry Root    :", software["registry_root"])
        print("-" * 70)

    print("\nInstalled software scan completed successfully.")
def print_usb_devices():
    """
    Print USB devices in readable format.
    """
    reader = USBDevicesReader()
    data = reader.read_usb_devices()

    print("=" * 70)
    print("USB Devices Scan")
    print("=" * 70)

    print("Total USB Devices Found:", data["total_usb_devices"])
    print("-" * 70)

    if data["total_usb_devices"] == 0:
        print("No USB storage devices found.")
        print("Try running PowerShell as Administrator.")
        return

    for index, usb in enumerate(data["usb_devices"], start=1):
        print(f"\nUSB Device #{index}")
        print("Device Name        :", usb["device_name"])
        print("Vendor             :", usb["vendor"])
        print("Product            :", usb["product"])
        print("Revision           :", usb["revision"])
        print("Serial Number      :", usb["serial_number"])
        print("Friendly Name      :", usb["friendly_name"])
        print("Device Description :", usb["device_description"])
        print("Manufacturer       :", usb["manufacturer"])
        print("Class GUID         :", usb["class_guid"])
        print("Last Write Time    :", usb["last_write_time"])
        print("Registry Root      :", usb["registry_root"])
        print("Registry Path      :", usb["registry_path"])
        print("-" * 70)

    print("\nUSB devices scan completed successfully.")    

def print_startup_programs():
    """
    Print startup programs in readable format.
    """
    reader = StartupProgramsReader()
    data = reader.get_startup_programs()

    print("=" * 70)
    print("Startup Programs Scan")
    print("=" * 70)

    print("Total Startup Programs Found:", data["total_startup_programs"])
    print("-" * 70)

    if data["total_startup_programs"] == 0:
        print("No startup programs found.")
        return
    def print_usb_devices():
        """
        Print USB devices in readable format.
        """
    reader = USBDevicesReader()
    data = reader.read_usb_devices()

    print("=" * 70)
    print("USB Devices Scan")
    print("=" * 70)

    print("Total USB Devices Found:", data["total_usb_devices"])
    print("-" * 70)

    if data["total_usb_devices"] == 0:
        print("No USB storage devices found.")
        print("Try running PowerShell as Administrator.")
        return

    for index, usb in enumerate(data["usb_devices"], start=1):
        print(f"\nUSB Device #{index}")
        print("Device Name        :", usb["device_name"])
        print("Vendor             :", usb["vendor"])
        print("Product            :", usb["product"])
        print("Revision           :", usb["revision"])
        print("Serial Number      :", usb["serial_number"])
        print("Friendly Name      :", usb["friendly_name"])
        print("Device Description :", usb["device_description"])
        print("Manufacturer       :", usb["manufacturer"])
        print("Class GUID         :", usb["class_guid"])
        print("Last Write Time    :", usb["last_write_time"])
        print("Registry Root      :", usb["registry_root"])
        print("Registry Path      :", usb["registry_path"])
        print("-" * 70)

    print("\nUSB devices scan completed successfully.")
    for index, program in enumerate(data["startup_programs"], start=1):
        print(f"\nStartup Program #{index}")
        print("Program Name  :", program["program_name"])
        print("Command       :", program["command"])
        print("Scope         :", program["scope"])
        print("Registry View :", program["registry_view"])
        print("Registry Root :", program["registry_root"])
        print("Value Type    :", program["value_type"])
        print("Registry Path :", program["registry_path"])
        print("-" * 70)

    print("\nStartup programs scan completed successfully.")
def print_user_activity():
    """
    Print user activity artifacts in readable format.
    """
    reader = UserActivityReader()
    data = reader.get_user_activity()

    print("=" * 70)
    print("User Activity Scan")
    print("=" * 70)

    print("RunMRU Commands Found :", data["runmru_count"])
    print("Typed Paths Found     :", data["typed_paths_count"])
    print("Recent Docs Found     :", data["recent_docs_count"])
    print("UserAssist Items Found:", data["userassist_count"])
    print("-" * 70)

    print("\nRunMRU Commands:")
    print("-" * 70)

    if not data["runmru"]:
        print("No RunMRU commands found.")
    else:
        for item in data["runmru"]:
            print("Command Name :", item["command_name"])
            print("Command      :", item["command"])
            print("Registry Path:", item["registry_path"])
            print("-" * 70)

    print("\nTyped Paths:")
    print("-" * 70)

    if not data["typed_paths"]:
        print("No typed paths found.")
    else:
        for item in data["typed_paths"]:
            print("Value Name   :", item["value_name"])
            print("Typed Path   :", item["typed_path"])
            print("Registry Path:", item["registry_path"])
            print("-" * 70)

    print("\nRecent Documents:")
    print("-" * 70)

    if not data["recent_docs"]:
        print("No recent documents found.")
    else:
        for item in data["recent_docs"][:30]:
            print("Category     :", item["category"])
            print("Value Name   :", item["value_name"])
            print("Recent Item  :", item["recent_item"])
            print("Registry Path:", item["registry_path"])
            print("-" * 70)

        if data["recent_docs_count"] > 30:
            print(f"Showing first 30 of {data['recent_docs_count']} recent documents.")

    print("\nUserAssist:")
    print("-" * 70)

    if not data["userassist"]:
        print("No UserAssist items found.")
    else:
        for item in data["userassist"][:30]:
            print("GUID         :", item["guid"])
            print("Decoded Name :", item["decoded_name"])
            print("Registry Path:", item["registry_path"])
            print("-" * 70)

        if data["userassist_count"] > 30:
            print(f"Showing first 30 of {data['userassist_count']} UserAssist items.")

    print("\nUser activity scan completed successfully.")
def main():
    while True:
        print("1. System Information")
        print("2. Installed Software")
        print("3. Startup Programs")
        print("4. USB Devices")
        print("5. User Activity")
        print("6. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            print_system_info()

        elif choice == "2":
            print_installed_software()

        elif choice == "3":
            print_startup_programs()

        elif choice == "4":
            print_usb_devices()

        elif choice == "5":
            print_user_activity()

        elif choice == "6":
            print("Exiting tool...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()