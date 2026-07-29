from registry_reader import RegistryReader
from important_paths import NTUSER_PATHS, SYSTEM_PATHS, SOFTWARE_PATHS


def print_values(values):
    """
    Print registry values in simple readable format.
    """
    if not values:
        print("No values found.")
        return

    for value in values:
        print(f"Name : {value['name']}")
        print(f"Type : {value['type']}")
        print(f"Data : {value['value']}")
        print("-" * 60)


def print_subkeys(subkeys):
    """
    Print registry subkeys in simple readable format.
    """
    if not subkeys:
        print("No subkeys found.")
        return

    for subkey in subkeys:
        print(f"Name      : {subkey['name']}")
        print(f"Path      : {subkey['path']}")
        print(f"Timestamp : {subkey['timestamp']}")
        print("-" * 60)


def print_artifact_data(data):
    """
    Print complete artifact output.
    """
    print("\n" + "=" * 70)
    print(f"Artifact    : {data['artifact_name']}")
    print(f"Source Hive : {data['source_hive']}")
    print(f"Source Path : {data['source_path']}")
    print("=" * 70)

    key_info = data["key_info"]

    if key_info["exists"] is False:
        print("Key Status  : Not Found")
        print("Message     :", key_info.get("message", "No message"))
        return

    print("Key Status  : Found")
    print("Key Name    :", key_info["name"])
    print("Timestamp   :", key_info["timestamp"])
    print("Values      :", key_info["total_values"])
    print("Subkeys     :", key_info["total_subkeys"])

    print("\nValues:")
    print("-" * 70)
    print_values(data["values"])

    print("\nSubkeys:")
    print("-" * 70)
    print_subkeys(data["subkeys"])


def test_ntuser():
    hive_path = input("Enter NTUSER.DAT path, example samples/NTUSER.DAT: ")

    reader = RegistryReader(hive_path)
    result = reader.load_hive()
    print("\n" + result["message"])

    if result["status"] is False:
        return

    for artifact_name, key_path in NTUSER_PATHS.items():
        data = reader.read_artifact_path(artifact_name, key_path)
        print_artifact_data(data)


def test_system():
    hive_path = input("Enter SYSTEM hive path, example samples/SYSTEM: ")

    reader = RegistryReader(hive_path)
    result = reader.load_hive()
    print("\n" + result["message"])

    if result["status"] is False:
        return

    for artifact_name, key_path in SYSTEM_PATHS.items():
        data = reader.read_artifact_path(artifact_name, key_path)
        print_artifact_data(data)


def test_software():
    hive_path = input("Enter SOFTWARE hive path, example samples/SOFTWARE: ")

    reader = RegistryReader(hive_path)
    result = reader.load_hive()
    print("\n" + result["message"])

    if result["status"] is False:
        return

    for artifact_name, key_path in SOFTWARE_PATHS.items():
        data = reader.read_artifact_path(artifact_name, key_path)
        print_artifact_data(data)


def main():
    print("=" * 70)
    print("Windows Registry Forensic Tool")
    print("Member 1 - Day 5 Important Registry Path Reader")
    print("=" * 70)

    print("\nSelect Hive Type:")
    print("1. NTUSER.DAT")
    print("2. SYSTEM")
    print("3. SOFTWARE")

    choice = input("\nEnter choice: ")

    if choice == "1":
        test_ntuser()
    elif choice == "2":
        test_system()
    elif choice == "3":
        test_software()
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()