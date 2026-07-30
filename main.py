from backend.live_registry.system_info import SystemInfoReader


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


def main():
    print("\nSelect Option:")
    print("1. System Information")
    print("2. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        print_system_info()
    elif choice == "2":
        print("Exiting tool...")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()