from hive_loader import HiveLoader


def main():
    print("=" * 60)
    print("Windows Registry Forensic Tool")
    print("Member 1 - Hive Loader Test")
    print("=" * 60)

    hive_path = input("Enter hive path, example ../samples/NTUSER.DAT: ")

    loader = HiveLoader(hive_path)
    result = loader.load_hive()

    print("\n" + result["message"])

    if result["status"] is False:
        return

    print("\nRoot Subkeys:")
    print("-" * 60)

    subkeys = loader.list_root_subkeys()

    if not subkeys:
        print("No root subkeys found.")
    else:
        for subkey in subkeys:
            print(f"Name      : {subkey['name']}")
            print(f"Path      : {subkey['path']}")
            print(f"Timestamp : {subkey['timestamp']}")
            print("-" * 60)

    print("\nTest completed successfully.")


if __name__ == "__main__":
    main()