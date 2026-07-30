import winreg


class CommonRegistryReader:
    """
    Common Registry Reader using Windows winreg API.
    This class reads live registry data from current PC.
    """

    def __init__(self):
        self.root_keys = {
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKCR": winreg.HKEY_CLASSES_ROOT,
            "HKU": winreg.HKEY_USERS,
            "HKCC": winreg.HKEY_CURRENT_CONFIG,
        }

    def get_root_key(self, root_name):
        """
        Convert root key name into winreg root key.
        Example: HKLM -> HKEY_LOCAL_MACHINE
        """
        return self.root_keys.get(root_name)

    def read_values(self, root_name, registry_path):
        """
        Read all values from a registry key.
        """
        try:
            root_key = self.get_root_key(root_name)

            if root_key is None:
                return {
                    "status": False,
                    "message": "Invalid root key",
                    "values": []
                }

            key = winreg.OpenKey(root_key, registry_path, 0, winreg.KEY_READ)

            values = []
            index = 0

            while True:
                try:
                    name, data, data_type = winreg.EnumValue(key, index)

                    values.append({
                        "name": name,
                        "data": data,
                        "type": self.get_value_type_name(data_type)
                    })

                    index += 1

                except OSError:
                    break

            winreg.CloseKey(key)

            return {
                "status": True,
                "message": "Values read successfully",
                "root": root_name,
                "path": registry_path,
                "values": values
            }

        except PermissionError:
            return {
                "status": False,
                "message": "Permission denied. Run tool as Administrator.",
                "values": []
            }

        except FileNotFoundError:
            return {
                "status": False,
                "message": "Registry path not found.",
                "values": []
            }

        except Exception as error:
            return {
                "status": False,
                "message": str(error),
                "values": []
            }

    def read_subkeys(self, root_name, registry_path):
        """
        Read all subkeys from a registry key.
        """
        try:
            root_key = self.get_root_key(root_name)

            if root_key is None:
                return {
                    "status": False,
                    "message": "Invalid root key",
                    "subkeys": []
                }

            key = winreg.OpenKey(root_key, registry_path, 0, winreg.KEY_READ)

            subkeys = []
            index = 0

            while True:
                try:
                    subkey_name = winreg.EnumKey(key, index)
                    subkeys.append(subkey_name)
                    index += 1

                except OSError:
                    break

            winreg.CloseKey(key)

            return {
                "status": True,
                "message": "Subkeys read successfully",
                "root": root_name,
                "path": registry_path,
                "subkeys": subkeys
            }

        except PermissionError:
            return {
                "status": False,
                "message": "Permission denied. Run tool as Administrator.",
                "subkeys": []
            }

        except FileNotFoundError:
            return {
                "status": False,
                "message": "Registry path not found.",
                "subkeys": []
            }

        except Exception as error:
            return {
                "status": False,
                "message": str(error),
                "subkeys": []
            }

    def get_single_value(self, root_name, registry_path, value_name):
        """
        Read one specific value from a registry key.
        """
        try:
            root_key = self.get_root_key(root_name)

            if root_key is None:
                return None

            key = winreg.OpenKey(root_key, registry_path, 0, winreg.KEY_READ)
            value, value_type = winreg.QueryValueEx(key, value_name)
            winreg.CloseKey(key)

            return value

        except Exception:
            return None

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