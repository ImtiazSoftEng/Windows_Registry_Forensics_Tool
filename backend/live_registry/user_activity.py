import winreg
import codecs
import re


class UserActivityReader:
    """
    Reads current user activity from live Windows Registry using winreg.

    Main hive:
    HKCU = HKEY_CURRENT_USER
    """

    def __init__(self):
        self.root = winreg.HKEY_CURRENT_USER
        self.root_name = "HKCU"

        self.runmru_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"
        self.typedpaths_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths"
        self.recentdocs_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs"
        self.userassist_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"

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

    def extract_text_from_binary(self, data):
        """
        Try to extract readable text from binary registry data.
        RecentDocs mostly stores file names in binary form.
        """
        try:
            if not isinstance(data, bytes):
                return data

            text = data.decode("utf-16le", errors="ignore")
            text = text.replace("\x00", " ")

            # Keep readable words, filenames, extensions
            parts = re.findall(r"[A-Za-z0-9_\- .()&]+(?:\.[A-Za-z0-9]{2,6})?", text)

            clean_parts = []

            for part in parts:
                part = part.strip()

                if len(part) >= 3 and part not in clean_parts:
                    clean_parts.append(part)

            if clean_parts:
                return " | ".join(clean_parts[:5])

            return data.hex()

        except Exception:
            return data.hex()

    def read_values_from_key(self, registry_path):
        """
        Read values from any HKCU registry key.
        """
        values = []

        try:
            key = winreg.OpenKey(
                self.root,
                registry_path,
                0,
                winreg.KEY_READ
            )

            index = 0

            while True:
                try:
                    name, data, value_type = winreg.EnumValue(key, index)

                    values.append({
                        "name": name,
                        "data": self.extract_text_from_binary(data),
                        "type": self.get_value_type_name(value_type),
                        "registry_root": self.root_name,
                        "registry_path": registry_path
                    })

                    index += 1

                except OSError:
                    break

            winreg.CloseKey(key)

        except FileNotFoundError:
            pass

        except PermissionError:
            print(f"Permission denied: {self.root_name}\\{registry_path}")

        except Exception as error:
            print(f"Error reading values: {error}")

        return values

    def read_subkeys(self, registry_path):
        """
        Read subkeys from any HKCU registry key.
        """
        subkeys = []

        try:
            key = winreg.OpenKey(
                self.root,
                registry_path,
                0,
                winreg.KEY_READ
            )

            index = 0

            while True:
                try:
                    subkey_name = winreg.EnumKey(key, index)
                    subkeys.append(subkey_name)
                    index += 1

                except OSError:
                    break

            winreg.CloseKey(key)

        except FileNotFoundError:
            pass

        except Exception:
            pass

        return subkeys

    def read_runmru(self):
        """
        Read commands typed in Windows Run box.
        """
        values = self.read_values_from_key(self.runmru_path)

        run_commands = []

        for item in values:
            if item["name"] != "MRUList":
                run_commands.append({
                    "command_name": item["name"],
                    "command": item["data"],
                    "type": item["type"],
                    "registry_path": item["registry_path"]
                })

        return run_commands

    def read_typed_paths(self):
        """
        Read paths typed in File Explorer address bar.
        """
        values = self.read_values_from_key(self.typedpaths_path)

        typed_paths = []

        for item in values:
            typed_paths.append({
                "value_name": item["name"],
                "typed_path": item["data"],
                "type": item["type"],
                "registry_path": item["registry_path"]
            })

        return typed_paths

    def read_recent_docs(self):
        """
        Read recently opened documents/files.
        """
        recent_docs = []

        # Parent RecentDocs values
        parent_values = self.read_values_from_key(self.recentdocs_path)

        for item in parent_values:
            if item["name"] != "MRUListEx":
                recent_docs.append({
                    "category": "General",
                    "value_name": item["name"],
                    "recent_item": item["data"],
                    "type": item["type"],
                    "registry_path": item["registry_path"]
                })

        # Extension subkeys like .pdf, .docx, .png
        subkeys = self.read_subkeys(self.recentdocs_path)

        for subkey in subkeys:
            subkey_path = self.recentdocs_path + "\\" + subkey
            values = self.read_values_from_key(subkey_path)

            for item in values:
                if item["name"] != "MRUListEx":
                    recent_docs.append({
                        "category": subkey,
                        "value_name": item["name"],
                        "recent_item": item["data"],
                        "type": item["type"],
                        "registry_path": item["registry_path"]
                    })

        return recent_docs

    def decode_rot13(self, text):
        """
        Decode UserAssist ROT13 encoded names.
        """
        try:
            return codecs.decode(text, "rot_13")
        except Exception:
            return text

    def read_userassist(self):
        """
        Read UserAssist program execution traces.
        UserAssist value names are usually ROT13 encoded.
        """
        userassist_items = []

        guid_subkeys = self.read_subkeys(self.userassist_path)

        for guid in guid_subkeys:
            count_path = self.userassist_path + "\\" + guid + "\\Count"
            values = self.read_values_from_key(count_path)

            for item in values:
                decoded_name = self.decode_rot13(item["name"])

                userassist_items.append({
                    "guid": guid,
                    "encoded_name": item["name"],
                    "decoded_name": decoded_name,
                    "type": item["type"],
                    "registry_path": item["registry_path"]
                })

        return userassist_items

    def get_user_activity(self):
        """
        Final clean output for user activity.
        """
        runmru = self.read_runmru()
        typed_paths = self.read_typed_paths()
        recent_docs = self.read_recent_docs()
        userassist = self.read_userassist()

        return {
            "artifact_name": "User Activity",
            "runmru_count": len(runmru),
            "typed_paths_count": len(typed_paths),
            "recent_docs_count": len(recent_docs),
            "userassist_count": len(userassist),
            "runmru": runmru,
            "typed_paths": typed_paths,
            "recent_docs": recent_docs,
            "userassist": userassist
        }