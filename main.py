from backend.live_registry.system_info import SystemInfoReader
from backend.live_registry.installed_software import InstalledSoftwareReader
from backend.live_registry.startup_programs import StartupProgramsReader

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
def main():
    while True:
        print("1. System Information")
        print("2. Installed Software")
        print("3. Startup Programs")
        print("4. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            print_system_info()

        elif choice == "2":
            print_installed_software()

        elif choice == "3":
            print_startup_programs()

        elif choice == "4":
            print("Exiting tool...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()