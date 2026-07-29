from Registry import Registry
from pathlib import Path


class RegistryReader:
    """
    Member 1: Registry Reader

    This class reads specific registry paths from offline hive files.
    It gives clean output for Member 2 artifact modules.
    """

    def __init__(self, hive_path):
        self.hive_path = Path(hive_path)
        self.registry = None

    def load_hive(self):
        """
        Load registry hive file.
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

    def open_key(self, key_path):
        """
        Open a specific registry key path safely.
        """
        try:
            if self.registry is None:
                return None

            return self.registry.open(key_path)

        except Exception:
            return None

    def key_exists(self, key_path):
        """
        Check whether a registry path exists or not.
        """
        key = self.open_key(key_path)

        if key is None:
            return False

        return True

    def clean_value(self, data):
        """
        Convert registry data into readable format.
        """
        try:
            if isinstance(data, bytes):
                return data.hex()

            if isinstance(data, list):
                return [str(item) for item in data]

            return data

        except Exception:
            return None

    def list_values(self, key_path):
        """
        Read all values from a registry key.
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
            print(f"Error reading values: {error}")
            return []

    def list_subkeys(self, key_path):
        """
        Read all subkeys from a registry key.
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
            print(f"Error reading subkeys: {error}")
            return []

    def get_key_info(self, key_path):
        """
        Get basic information of a registry key.
        """
        try:
            key = self.open_key(key_path)

            if key is None:
                return {
                    "exists": False,
                    "message": "Key not found",
                    "path": key_path
                }

            return {
                "exists": True,
                "name": key.name(),
                "path": key.path(),
                "timestamp": str(key.timestamp()),
                "total_values": len(key.values()),
                "total_subkeys": len(key.subkeys())
            }

        except Exception as error:
            return {
                "exists": False,
                "message": str(error),
                "path": key_path
            }

    def read_artifact_path(self, artifact_name, key_path):
        """
        Standard output format for Member 2.

        This function reads:
        - key information
        - values
        - subkeys
        """
        return {
            "artifact_name": artifact_name,
            "source_hive": self.hive_path.name,
            "source_path": key_path,
            "key_info": self.get_key_info(key_path),
            "values": self.list_values(key_path),
            "subkeys": self.list_subkeys(key_path)
        }