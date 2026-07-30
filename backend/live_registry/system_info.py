import os
import platform
import ctypes
from backend.live_registry.common_reader import CommonRegistryReader
from datetime import datetime


class SystemInfoReader:
    """
    Reads live Windows system information from registry and OS.
    """

    def __init__(self):
        self.reader = CommonRegistryReader()

    def is_admin(self):
        """
        Check if tool is running as Administrator.
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def get_windows_info(self):
        """
        Read Windows version information from registry.
        """
        path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"

        product_name = self.reader.get_single_value("HKLM", path, "ProductName")
        display_version = self.reader.get_single_value("HKLM", path, "DisplayVersion")
        current_build = self.reader.get_single_value("HKLM", path, "CurrentBuild")
        ubr = self.reader.get_single_value("HKLM", path, "UBR")
        edition_id = self.reader.get_single_value("HKLM", path, "EditionID")
        install_date_raw = self.reader.get_single_value("HKLM", path, "InstallDate")
        install_date = self.convert_timestamp(install_date_raw)
        system_root = self.reader.get_single_value("HKLM", path, "SystemRoot")

        return {
            "product_name": product_name,
            "display_version": display_version,
            "current_build": current_build,
            "ubr": ubr,
            "edition_id": edition_id,
            "install_date": install_date,
            "system_root": system_root
        }

    def get_computer_name(self):
        """
        Read computer name from registry.
        """
        path = r"SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName"

        computer_name = self.reader.get_single_value("HKLM", path, "ComputerName")

        return computer_name

    def get_timezone_info(self):
        """
        Read timezone information from registry.
        """
        path = r"SYSTEM\CurrentControlSet\Control\TimeZoneInformation"

        time_zone = self.reader.get_single_value("HKLM", path, "TimeZoneKeyName")
        standard_name = self.reader.get_single_value("HKLM", path, "StandardName")

        return {
            "time_zone": time_zone,
            "standard_name": standard_name
        }
    

    def convert_timestamp(self, timestamp):
        """
        Convert Windows InstallDate timestamp into readable date.
        """
        try:
            if timestamp is None:
                return None

            return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")

        except Exception:
            return timestamp
    def get_current_user_info(self):
        """
        Read current logged-in user information.
        """
        return {
            "username": os.environ.get("USERNAME"),
            "user_domain": os.environ.get("USERDOMAIN"),
            "user_profile": os.environ.get("USERPROFILE"),
            "computer_name_env": os.environ.get("COMPUTERNAME")
        }

    def get_system_info(self):
        """
        Final clean output for system information.
        """
        windows_info = self.get_windows_info()
        timezone_info = self.get_timezone_info()
        user_info = self.get_current_user_info()

        return {
            "tool_mode": "Live Registry Analysis",
            "admin_status": self.is_admin(),
            "computer_name": self.get_computer_name(),
            "windows_info": windows_info,
            "timezone_info": timezone_info,
            "user_info": user_info,
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "machine": platform.machine()
        }
    