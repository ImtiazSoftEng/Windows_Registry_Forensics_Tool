import winreg


class StartupProgramsReader:
    """
    Reads startup programs from live Windows Registry using winreg.
    """

    def __init__(self):
        self.startup_locations = [
            {
                "root": winreg.HKEY_LOCAL_MACHINE,
                "root_name": "HKLM",
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                "scope": "All Users",
                "view": "64-bit"
            },
            {
                "root": winreg.HKEY_LOCAL_MACHINE,
                "root_name": "HKLM",
                "path": r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run",
                "scope": "All Users",
                "view": "32-bit"
            },
            {
                "root": winreg.HKEY_CURRENT_USER,
                "root_name": "HKCU",
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                "scope": "Current User",
                "view": "User"
            }
        ]

    def get_value_type_name(self, value_type):
        """
        Convert registry value type into readable name.
        """
        types = {
            winreg.REG_SZ: "REG_SZ",
            winreg.REG_DWORD: "REG_DWORD",
            winreg.REG_BINARY: "REG_BINARY",
            winreg.REG_MULTI_SZ: "REG_MULTI_SZ",
            winreg.REG_EXPAND_SZ: "REG_EXPAND_SZ",
            winreg.REG_QWORD: "REG_QWORD",
        }

        return types.get(value_type, str(value_type))

    def read_startup_from_location(self, location):
        """
        Read startup programs from one registry location.
        """
        startup_list = []

        try:
            key = winreg.OpenKey(
                location["root"],
                location["path"],
                0,
                winreg.KEY_READ
            )

            index = 0

            while True:
                try:
                    name, command, value_type = winreg.EnumValue(key, index)

                    startup_info = {
                        "program_name": name,
                        "command": command,
                        "scope": location["scope"],
                        "registry_view": location["view"],
                        "registry_root": location["root_name"],
                        "registry_path": location["path"],
                        "value_type": self.get_value_type_name(value_type)
                    }

                    startup_list.append(startup_info)
                    index += 1

                except OSError:
                    break

            winreg.CloseKey(key)

        except FileNotFoundError:
            pass

        except PermissionError:
            print(f"Permission denied: {location['root_name']}\\{location['path']}")

        except Exception as error:
            print(f"Error reading startup programs: {error}")

        return startup_list

    def get_startup_programs(self):
        """
        Final function to collect startup programs from all locations.
        """
        all_startup_programs = []

        for location in self.startup_locations:
            startup_programs = self.read_startup_from_location(location)
            all_startup_programs.extend(startup_programs)

        return {
            "artifact_name": "Startup Programs",
            "total_startup_programs": len(all_startup_programs),
            "startup_programs": all_startup_programs
        }