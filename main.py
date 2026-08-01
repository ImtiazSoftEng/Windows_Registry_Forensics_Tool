from datetime import datetime

from backend.live_registry.system_info import SystemInfoReader
from backend.live_registry.installed_software import InstalledSoftwareReader
from backend.live_registry.startup_programs import StartupProgramsReader
from backend.live_registry.usb_devices import USBDevicesReader
from backend.live_registry.user_activity import UserActivityReader

from backend.reports.json_export import JSONExport
from backend.reports.csv_export import CSVExport


def print_system_info():
    reader = SystemInfoReader()
    data = reader.get_system_info()

    print("=" * 70)
    print("System Information Scan")
    print("=" * 70)

    print("Admin Status     :", data.get("admin_status"))
    print("Computer Name    :", data.get("computer_name"))
    print("Architecture     :", data.get("architecture"))
    print("Machine          :", data.get("machine"))
    print("Processor        :", data.get("processor"))

    windows = data.get("windows_info", {})
    print("\nWindows Information:")
    print("Product Name     :", windows.get("product_name"))
    print("Display Version  :", windows.get("display_version"))
    print("Build Number     :", windows.get("current_build"))
    print("UBR              :", windows.get("ubr"))
    print("Edition ID       :", windows.get("edition_id"))
    print("Install Date     :", windows.get("install_date"))
    print("System Root      :", windows.get("system_root"))

    user = data.get("user_info", {})
    print("\nCurrent User:")
    print("Username         :", user.get("username"))
    print("User Domain      :", user.get("user_domain"))
    print("User Profile     :", user.get("user_profile"))

    timezone = data.get("timezone_info", {})
    print("\nTimezone:")
    print("Time Zone        :", timezone.get("time_zone"))
    print("Standard Name    :", timezone.get("standard_name"))

    print("\nSystem information scan completed successfully.")


def print_installed_software():
    reader = InstalledSoftwareReader()
    data = reader.get_installed_software()

    print("=" * 70)
    print("Installed Software Scan")
    print("=" * 70)

    software_list = data.get("software_list", [])

    print("Total Programs Found:", data.get("total_programs", 0))
    print("-" * 70)

    if not software_list:
        print("No installed software found.")
        return

    for index, software in enumerate(software_list, start=1):
        print(f"\nProgram #{index}")
        print("Name             :", software.get("name"))
        print("Version          :", software.get("version"))
        print("Publisher        :", software.get("publisher"))
        print("Install Date     :", software.get("install_date"))
        print("Install Location :", software.get("install_location"))
        print("Registry View    :", software.get("registry_view"))
        print("Registry Root    :", software.get("registry_root"))
        print("-" * 70)

    print("\nInstalled software scan completed successfully.")


def print_startup_programs():
    reader = StartupProgramsReader()
    data = reader.get_startup_programs()

    print("=" * 70)
    print("Startup Programs Scan")
    print("=" * 70)

    startup_programs = data.get("startup_programs", [])

    print("Total Startup Programs Found:", data.get("total_startup_programs", 0))
    print("-" * 70)

    if not startup_programs:
        print("No startup programs found.")
        return

    for index, program in enumerate(startup_programs, start=1):
        print(f"\nStartup Program #{index}")
        print("Program Name  :", program.get("program_name"))
        print("Command       :", program.get("command"))
        print("Scope         :", program.get("scope"))
        print("Registry View :", program.get("registry_view"))
        print("Registry Root :", program.get("registry_root"))
        print("Value Type    :", program.get("value_type"))
        print("Registry Path :", program.get("registry_path"))
        print("-" * 70)

    print("\nStartup programs scan completed successfully.")


def print_usb_devices():
    reader = USBDevicesReader()
    data = reader.read_usb_devices()

    print("=" * 70)
    print("USB Devices Scan")
    print("=" * 70)

    usb_devices = data.get("usb_devices", [])

    print("Total USB Devices Found:", data.get("total_usb_devices", 0))
    print("-" * 70)

    if not usb_devices:
        print("No USB storage devices found.")
        print("Try running PowerShell as Administrator.")
        return

    for index, usb in enumerate(usb_devices, start=1):
        print(f"\nUSB Device #{index}")
        print("Device Name        :", usb.get("device_name"))
        print("Vendor             :", usb.get("vendor"))
        print("Product            :", usb.get("product"))
        print("Revision           :", usb.get("revision"))
        print("Serial Number      :", usb.get("serial_number"))
        print("Friendly Name      :", usb.get("friendly_name"))
        print("Device Description :", usb.get("device_description"))
        print("Manufacturer       :", usb.get("manufacturer"))
        print("Class GUID         :", usb.get("class_guid"))
        print("Last Write Time    :", usb.get("last_write_time"))
        print("Registry Root      :", usb.get("registry_root"))
        print("Registry Path      :", usb.get("registry_path"))
        print("-" * 70)

    print("\nUSB devices scan completed successfully.")


def print_user_activity():
    reader = UserActivityReader()
    data = reader.get_user_activity()

    print("=" * 70)
    print("User Activity Scan")
    print("=" * 70)

    print("RunMRU Commands Found :", data.get("runmru_count", 0))
    print("Typed Paths Found     :", data.get("typed_paths_count", 0))
    print("Recent Docs Found     :", data.get("recent_docs_count", 0))
    print("UserAssist Items Found:", data.get("userassist_count", 0))
    print("-" * 70)

    print("\nRunMRU Commands:")
    print("-" * 70)

    for item in data.get("runmru", []):
        print("Command Name :", item.get("command_name"))
        print("Command      :", item.get("command"))
        print("Registry Path:", item.get("registry_path"))
        print("-" * 70)

    print("\nTyped Paths:")
    print("-" * 70)

    for item in data.get("typed_paths", []):
        print("Value Name   :", item.get("value_name"))
        print("Typed Path   :", item.get("typed_path"))
        print("Registry Path:", item.get("registry_path"))
        print("-" * 70)

    print("\nRecent Documents:")
    print("-" * 70)

    recent_docs = data.get("recent_docs", [])

    for item in recent_docs[:30]:
        print("Category     :", item.get("category"))
        print("Value Name   :", item.get("value_name"))
        print("Recent Item  :", item.get("recent_item"))
        print("Registry Path:", item.get("registry_path"))
        print("-" * 70)

    if len(recent_docs) > 30:
        print(f"Showing first 30 of {len(recent_docs)} recent documents.")

    print("\nUserAssist:")
    print("-" * 70)

    userassist = data.get("userassist", [])

    for item in userassist[:30]:
        print("GUID         :", item.get("guid"))
        print("Decoded Name :", item.get("decoded_name"))
        print("Registry Path:", item.get("registry_path"))
        print("-" * 70)

    if len(userassist) > 30:
        print(f"Showing first 30 of {len(userassist)} UserAssist items.")

    print("\nUser activity scan completed successfully.")


def generate_full_report():
    print("=" * 70)
    print("Full Registry Scan Started")
    print("=" * 70)

    print("Collecting system information...")
    system_info = SystemInfoReader().get_system_info()

    print("Collecting installed software...")
    installed_software = InstalledSoftwareReader().get_installed_software()

    print("Collecting startup programs...")
    startup_programs = StartupProgramsReader().get_startup_programs()

    print("Collecting USB devices...")
    usb_devices = USBDevicesReader().read_usb_devices()

    print("Collecting user activity...")
    user_activity = UserActivityReader().get_user_activity()

    report_data = {
        "tool_name": "Portable Windows Registry Forensic Analyzer",
        "tool_mode": "Live Registry Analysis",
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_info": system_info,
        "installed_software": installed_software,
        "startup_programs": startup_programs,
        "usb_devices": usb_devices,
        "user_activity": user_activity
    }

    print("\nSaving JSON report...")
    json_exporter = JSONExport()
    json_result = json_exporter.save_json(report_data)

    print(json_result.get("message"))
    print("JSON Path:", json_result.get("file_path"))

    print("\nSaving CSV reports...")
    csv_exporter = CSVExport()
    csv_results = csv_exporter.save_all_csv_reports(report_data)

    for result in csv_results:
        print(result.get("message"), "->", result.get("file_path"))

    print("\nFull report generation completed successfully.")


def main():
    while True:
        print("\n1. System Information")
        print("2. Installed Software")
        print("3. Startup Programs")
        print("4. USB Devices")
        print("5. User Activity")
        print("6. Generate Full Report")
        print("7. Exit")

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
            generate_full_report()

        elif choice == "7":
            print("Exiting tool...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()