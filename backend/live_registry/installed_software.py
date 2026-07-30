import winreg


class InstalledSoftwareReader:
    """
    Reads installed software from live Windows Registry using winreg.
    """

    def __init__(self):
        self.uninstall_locations = [
            {
                "root": winreg.HKEY_LOCAL_MACHINE,
                "root_name": "HKLM",
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                "view": "64-bit"
            },
            {
                "root": winreg.HKEY_LOCAL_MACHINE,
                "root_name": "HKLM",
                "path": r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
                "view": "32-bit"
            },
            {
                "root": winreg.HKEY_CURRENT_USER,
                "root_name": "HKCU",
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                "view": "Current User"
            }
        ]

    def get_value(self, registry_key, value_name):
        """
        Read one value from opened registry key.
        If value is missing, return None.
        """
        try:
            value, value_type = winreg.QueryValueEx(registry_key, value_name)
            return value
        except Exception:
            return None

    def format_install_date(self, install_date):
        """
        Convert install date from YYYYMMDD to YYYY-MM-DD.
        Example: 20250115 -> 2025-01-15
        """
        try:
            if install_date is None:
                return None

            install_date = str(install_date)

            if len(install_date) == 8:
                year = install_date[0:4]
                month = install_date[4:6]
                day = install_date[6:8]
                return f"{year}-{month}-{day}"

            return install_date

        except Exception:
            return install_date

    def read_software_from_location(self, location):
        """
        Read installed software from one uninstall registry location.
        """
        software_list = []

        try:
            uninstall_key = winreg.OpenKey(
                location["root"],
                location["path"],
                0,
                winreg.KEY_READ
            )

            index = 0

            while True:
                try:
                    subkey_name = winreg.EnumKey(uninstall_key, index)
                    subkey_path = location["path"] + "\\" + subkey_name

                    try:
                        software_key = winreg.OpenKey(
                            location["root"],
                            subkey_path,
                            0,
                            winreg.KEY_READ
                        )

                        display_name = self.get_value(software_key, "DisplayName")

                        # Skip entries without software name
                        if display_name:
                            software_info = {
                                "name": display_name,
                                "version": self.get_value(software_key, "DisplayVersion"),
                                "publisher": self.get_value(software_key, "Publisher"),
                                "install_date": self.format_install_date(
                                    self.get_value(software_key, "InstallDate")
                                ),
                                "install_location": self.get_value(software_key, "InstallLocation"),
                                "uninstall_string": self.get_value(software_key, "UninstallString"),
                                "registry_root": location["root_name"],
                                "registry_view": location["view"],
                                "registry_path": subkey_path
                            }

                            software_list.append(software_info)

                        winreg.CloseKey(software_key)

                    except Exception:
                        pass

                    index += 1

                except OSError:
                    break

            winreg.CloseKey(uninstall_key)

        except PermissionError:
            print(f"Permission denied: {location['root_name']}\\{location['path']}")

        except FileNotFoundError:
            print(f"Path not found: {location['root_name']}\\{location['path']}")

        except Exception as error:
            print(f"Error reading installed software: {error}")

        return software_list

    def remove_duplicates(self, software_list):
        """
        Remove duplicate software entries.
        """
        unique_list = []
        seen = set()

        for software in software_list:
            key = (
                str(software.get("name")),
                str(software.get("version")),
                str(software.get("publisher"))
            )

            if key not in seen:
                seen.add(key)
                unique_list.append(software)

        return unique_list

    def get_installed_software(self):
        """
        Final function to collect installed software from all locations.
        """
        all_software = []

        for location in self.uninstall_locations:
            software = self.read_software_from_location(location)
            all_software.extend(software)

        all_software = self.remove_duplicates(all_software)

        return {
            "artifact_name": "Installed Software",
            "total_programs": len(all_software),
            "software_list": all_software
        }