import winreg
from datetime import datetime, timezone


class USBDevicesReader:
    """
    Reads USB storage and mounted device details from live Windows Registry.
    """

    def __init__(self):
        self.root = winreg.HKEY_LOCAL_MACHINE
        self.root_name = "HKLM"
        self.usbstor_path = r"SYSTEM\CurrentControlSet\Enum\USBSTOR"
        self.mounted_devices_path = r"SYSTEM\MountedDevices"

    def convert_windows_filetime(self, filetime):
        try:
            if not filetime:
                return None

            unix_time = (filetime - 116444736000000000) / 10000000
            return datetime.fromtimestamp(unix_time, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        except Exception:
            return None

    def get_key_last_write_time(self, registry_key):
        try:
            info = winreg.QueryInfoKey(registry_key)
            last_write_time = info[2]
            return self.convert_windows_filetime(last_write_time)

        except Exception:
            return None

    def get_value(self, registry_key, value_name):
        try:
            value, value_type = winreg.QueryValueEx(registry_key, value_name)
            return value

        except Exception:
            return None

    def parse_usb_device_name(self, device_name):
        vendor = None
        product = None
        revision = None

        try:
            parts = device_name.split("&")

            for part in parts:
                if part.startswith("Ven_"):
                    vendor = part.replace("Ven_", "")

                elif part.startswith("Prod_"):
                    product = part.replace("Prod_", "")

                elif part.startswith("Rev_"):
                    revision = part.replace("Rev_", "")

        except Exception:
            pass

        return {
            "vendor": vendor,
            "product": product,
            "revision": revision
        }

    def read_usbstor_devices(self):
        """
        Read USB storage devices from USBSTOR.
        """
        usb_devices = []

        try:
            usbstor_key = winreg.OpenKey(
                self.root,
                self.usbstor_path,
                0,
                winreg.KEY_READ
            )

            device_index = 0

            while True:
                try:
                    device_name = winreg.EnumKey(usbstor_key, device_index)
                    device_path = self.usbstor_path + "\\" + device_name
                    parsed_name = self.parse_usb_device_name(device_name)

                    device_key = winreg.OpenKey(
                        self.root,
                        device_path,
                        0,
                        winreg.KEY_READ
                    )

                    instance_index = 0

                    while True:
                        try:
                            serial_number = winreg.EnumKey(device_key, instance_index)
                            instance_path = device_path + "\\" + serial_number

                            instance_key = winreg.OpenKey(
                                self.root,
                                instance_path,
                                0,
                                winreg.KEY_READ
                            )

                            usb_info = {
                                "source": "USBSTOR",
                                "device_name": device_name,
                                "vendor": parsed_name["vendor"],
                                "product": parsed_name["product"],
                                "revision": parsed_name["revision"],
                                "serial_number": serial_number,
                                "friendly_name": self.get_value(instance_key, "FriendlyName"),
                                "device_description": self.get_value(instance_key, "DeviceDesc"),
                                "manufacturer": self.get_value(instance_key, "Mfg"),
                                "class_guid": self.get_value(instance_key, "ClassGUID"),
                                "last_write_time": self.get_key_last_write_time(instance_key),
                                "registry_root": self.root_name,
                                "registry_path": instance_path
                            }

                            usb_devices.append(usb_info)

                            winreg.CloseKey(instance_key)
                            instance_index += 1

                        except OSError:
                            break

                    winreg.CloseKey(device_key)
                    device_index += 1

                except OSError:
                    break

            winreg.CloseKey(usbstor_key)

        except FileNotFoundError:
            pass

        except PermissionError:
            print("Permission denied for USBSTOR. Run tool as Administrator.")

        except Exception as error:
            print(f"Error reading USBSTOR: {error}")

        return usb_devices

    def read_mounted_devices(self):
        """
        Read mounted drive/device entries.
        This is backup evidence when USBSTOR is empty or missing.
        """
        mounted_devices = []

        try:
            key = winreg.OpenKey(
                self.root,
                self.mounted_devices_path,
                0,
                winreg.KEY_READ
            )

            index = 0

            while True:
                try:
                    name, data, value_type = winreg.EnumValue(key, index)

                    mounted_info = {
                        "source": "MountedDevices",
                        "device_name": name,
                        "vendor": None,
                        "product": None,
                        "revision": None,
                        "serial_number": None,
                        "friendly_name": None,
                        "device_description": "Mounted device or drive mapping",
                        "manufacturer": None,
                        "class_guid": None,
                        "last_write_time": self.get_key_last_write_time(key),
                        "registry_root": self.root_name,
                        "registry_path": self.mounted_devices_path
                    }

                    mounted_devices.append(mounted_info)
                    index += 1

                except OSError:
                    break

            winreg.CloseKey(key)

        except FileNotFoundError:
            pass

        except PermissionError:
            print("Permission denied for MountedDevices. Run tool as Administrator.")

        except Exception as error:
            print(f"Error reading MountedDevices: {error}")

        return mounted_devices

    def read_usb_devices(self):
        """
        Final function to collect USB-related evidence.
        """
        usbstor_devices = self.read_usbstor_devices()
        mounted_devices = self.read_mounted_devices()

        all_devices = usbstor_devices + mounted_devices

        return {
            "artifact_name": "USB Devices",
            "total_usb_devices": len(all_devices),
            "usbstor_count": len(usbstor_devices),
            "mounted_devices_count": len(mounted_devices),
            "usb_devices": all_devices
        }