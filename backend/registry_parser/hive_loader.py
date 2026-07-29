from Registry import Registry
from pathlib import Path


class HiveLoader:
    """
    Member 1: Registry Parser
    This class loads offline Windows registry hive files:
    NTUSER.DAT, SYSTEM, SOFTWARE.
    """

    def __init__(self, hive_path):
        self.hive_path = Path(hive_path)
        self.registry = None

    def load_hive(self):
        """
        Load registry hive safely.
        """
        try:
            if not self.hive_path.exists():
                return {
                    "status": False,
                    "message": f"Hive file not found: {self.hive_path}"
                }

            self.registry = Registry.Registry(str(self.hive_path))

            return {
                "status": True,
                "message": "Hive loaded successfully",
                "hive_name": self.hive_path.name
            }

        except Exception as error:
            return {
                "status": False,
                "message": f"Error loading hive: {error}"
            }

    def list_root_subkeys(self):
        """
        List root-level registry keys.
        Example:
        NTUSER.DAT usually shows Software.
        SYSTEM usually shows ControlSet001, Select, MountedDevices.
        SOFTWARE usually shows Microsoft, Classes.
        """
        try:
            if self.registry is None:
                return []

            root = self.registry.root()
            results = []

            for subkey in root.subkeys():
                results.append({
                    "name": subkey.name(),
                    "path": subkey.path(),
                    "timestamp": str(subkey.timestamp())
                })

            return results

        except Exception as error:
            print(f"Error listing root subkeys: {error}")
            return []

    def open_key(self, key_path):
        """
        Open a registry key safely.
        """
        try:
            if self.registry is None:
                return None

            return self.registry.open(key_path)

        except Exception:
            return None

    def list_values(self, key_path):
        """
        List values from a specific registry key.
        """
        try:
            key = self.open_key(key_path)

            if key is None:
                return []

            values = []

            for value in key.values():
                values.append({
                    "name": value.name(),
                    "type": str(value.value_type()),
                    "value": self.clean_value(value.value())
                })

            return values

        except Exception as error:
            print(f"Error listing values: {error}")
            return []

    def list_subkeys(self, key_path):
        """
        List subkeys from a specific registry key.
        """
        try:
            key = self.open_key(key_path)

            if key is None:
                return []

            subkeys = []

            for subkey in key.subkeys():
                subkeys.append({
                    "name": subkey.name(),
                    "path": subkey.path(),
                    "timestamp": str(subkey.timestamp())
                })

            return subkeys

        except Exception as error:
            print(f"Error listing subkeys: {error}")
            return []

    def clean_value(self, data):
        """
        Convert registry value into readable format.
        """
        if isinstance(data, bytes):
            return data.hex()

        if isinstance(data, list):
            return [str(item) for item in data]

        return data