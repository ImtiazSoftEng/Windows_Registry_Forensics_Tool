"""
Mock registry readers.

winreg only exists on Windows, so this app can't touch a real registry
when it's run on Linux/Mac during development. These classes expose the
EXACT same method names and return the EXACT same dict shapes as the
real classes in backend/live_registry/*, so app.py can import either
set interchangeably (see the IS_WINDOWS switch in app.py).

Nothing about the frontend or the routes needs to know which set is
active — swap happens once, at import time, based on platform.
"""

from datetime import datetime


class SystemInfoReader:
    def get_system_info(self):
        return {
            "tool_mode": "Dev / Mock Mode (non-Windows backend)",
            "admin_status": False,
            "computer_name": "DEV-LINUX-BOX",
            "windows_info": {
                "product_name": "Windows 11 Pro (simulated)",
                "display_version": "24H2",
                "current_build": "26100",
                "ubr": "2033",
                "edition_id": "Professional",
                "install_date": "2024-11-02 09:14:07",
                "system_root": "C:\\Windows"
            },
            "timezone_info": {
                "time_zone": "Pakistan Standard Time",
                "standard_name": "Pakistan Standard Time"
            },
            "user_info": {
                "username": "jefe",
                "user_domain": "DEV-LINUX-BOX",
                "user_profile": "C:\\Users\\jefe",
                "computer_name_env": "DEV-LINUX-BOX"
            },
            "architecture": "64bit",
            "processor": "Simulated processor (no winreg on this host)",
            "machine": "x86_64"
        }


class InstalledSoftwareReader:
    def get_installed_software(self):
        software_list = [
            {"name": "Google Chrome", "version": "126.0.6478.127", "publisher": "Google LLC",
             "install_date": "2024-03-11", "install_location": "C:\\Program Files\\Google\\Chrome\\Application\\",
             "uninstall_string": "MsiExec.exe /X{9D1234-AB56}", "registry_root": "HKLM",
             "registry_view": "64-bit", "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Chrome"},
            {"name": "7-Zip 23.01", "version": "23.01", "publisher": "Igor Pavlov",
             "install_date": "2024-01-22", "install_location": "C:\\Program Files\\7-Zip\\",
             "uninstall_string": "C:\\Program Files\\7-Zip\\Uninstall.exe", "registry_root": "HKLM",
             "registry_view": "64-bit", "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\7-Zip"},
            {"name": "Wireshark 4.2.5", "version": "4.2.5", "publisher": "The Wireshark developer community",
             "install_date": "2024-05-02", "install_location": "C:\\Program Files\\Wireshark\\",
             "uninstall_string": "C:\\Program Files\\Wireshark\\uninstall.exe", "registry_root": "HKLM",
             "registry_view": "64-bit", "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Wireshark"},
            {"name": "Python 3.12.4 (64-bit)", "version": "3.12.4150.0", "publisher": "Python Software Foundation",
             "install_date": "2024-06-18", "install_location": "C:\\Users\\jefe\\AppData\\Local\\Programs\\Python\\Python312\\",
             "uninstall_string": "MsiExec.exe /X{7A2211-CC90}", "registry_root": "HKLM",
             "registry_view": "64-bit", "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Python312"},
            {"name": "AnyDesk", "version": "8.0.12", "publisher": "AnyDesk Software GmbH",
             "install_date": "2024-02-09", "install_location": "C:\\Users\\jefe\\AppData\\Local\\AnyDesk\\",
             "uninstall_string": "C:\\Users\\jefe\\AppData\\Local\\AnyDesk\\AnyDesk.exe --uninstall", "registry_root": "HKCU",
             "registry_view": "Current User", "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AnyDesk"},
            {"name": "USB Disk Security", "version": "6.9", "publisher": "Zbshareware Lab",
             "install_date": "2023-12-14", "install_location": "C:\\Program Files (x86)\\USB Disk Security\\",
             "uninstall_string": "C:\\Program Files (x86)\\USB Disk Security\\unins000.exe", "registry_root": "HKLM",
             "registry_view": "32-bit", "registry_path": "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\USBDiskSecurity"},
        ]
        return {
            "artifact_name": "Installed Software",
            "total_programs": len(software_list),
            "software_list": software_list
        }


class StartupProgramsReader:
    def get_startup_programs(self):
        startup_programs = [
            {"program_name": "OneDrive", "command": "\"C:\\Users\\jefe\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe\" /background",
             "scope": "Current User", "registry_view": "User", "registry_root": "HKCU",
             "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", "value_type": "REG_SZ"},
            {"program_name": "SecurityHealth", "command": "%windir%\\system32\\SecurityHealthSystray.exe",
             "scope": "All Users", "registry_view": "64-bit", "registry_root": "HKLM",
             "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", "value_type": "REG_EXPAND_SZ"},
            {"program_name": "AnyDeskSvc", "command": "C:\\Users\\jefe\\AppData\\Local\\AnyDesk\\AnyDesk.exe --tray",
             "scope": "Current User", "registry_view": "User", "registry_root": "HKCU",
             "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", "value_type": "REG_SZ"},
            {"program_name": "RtkAudUService", "command": "\"C:\\Program Files\\Realtek\\Audio\\HDA\\RtkAudUService64.exe\" -background",
             "scope": "All Users", "registry_view": "64-bit", "registry_root": "HKLM",
             "registry_path": "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", "value_type": "REG_SZ"},
        ]
        return {
            "artifact_name": "Startup Programs",
            "total_startup_programs": len(startup_programs),
            "startup_programs": startup_programs
        }


class USBDevicesReader:
    def read_usb_devices(self):
        usb_devices = [
            {"source": "USBSTOR", "device_name": "Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00",
             "vendor": "SanDisk", "product": "Ultra", "revision": "1.00",
             "serial_number": "4C531001471024117234&0", "friendly_name": "SanDisk Ultra USB Device",
             "device_description": "Disk drive", "manufacturer": "Compatible USB storage device",
             "class_guid": "{4D36E967-E325-11CE-BFC1-08002BE10318}",
             "last_write_time": "2026-07-14 08:22:41 UTC", "registry_root": "HKLM",
             "registry_path": "SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\\Disk&Ven_SanDisk&Prod_Ultra&Rev_1.00\\4C531001471024117234&0"},
            {"source": "USBSTOR", "device_name": "Disk&Ven_Kingston&Prod_DataTraveler_3.0&Rev_PMAP",
             "vendor": "Kingston", "product": "DataTraveler_3.0", "revision": "PMAP",
             "serial_number": "60A44C3A1FCE1B9A1D0C0012", "friendly_name": "Kingston DataTraveler 3.0 USB Device",
             "device_description": "Disk drive", "manufacturer": "Kingston",
             "class_guid": "{4D36E967-E325-11CE-BFC1-08002BE10318}",
             "last_write_time": "2026-06-29 16:03:12 UTC", "registry_root": "HKLM",
             "registry_path": "SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\\Disk&Ven_Kingston&Prod_DataTraveler_3.0&Rev_PMAP\\60A44C3A1FCE1B9A1D0C0012"},
            {"source": "MountedDevices", "device_name": "\\DosDevices\\E:",
             "vendor": None, "product": None, "revision": None, "serial_number": None,
             "friendly_name": None, "device_description": "Mounted device or drive mapping",
             "manufacturer": None, "class_guid": None,
             "last_write_time": "2026-07-14 08:22:41 UTC", "registry_root": "HKLM",
             "registry_path": "SYSTEM\\MountedDevices"},
        ]
        usbstor_count = sum(1 for d in usb_devices if d["source"] == "USBSTOR")
        return {
            "artifact_name": "USB Devices",
            "total_usb_devices": len(usb_devices),
            "usbstor_count": usbstor_count,
            "mounted_devices_count": len(usb_devices) - usbstor_count,
            "usb_devices": usb_devices
        }


class UserActivityReader:
    def get_user_activity(self):
        runmru = [
            {"command_name": "a", "command": "cmd", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU"},
            {"command_name": "b", "command": "regedit", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU"},
            {"command_name": "c", "command": "\\\\192.168.1.14\\share", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU"},
        ]
        typed_paths = [
            {"value_name": "url1", "typed_path": "D:\\Evidence\\Case_014\\Exports", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths"},
            {"value_name": "url2", "typed_path": "\\\\NAS-01\\forensics\\images", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths"},
        ]
        recent_docs = [
            {"category": ".pdf", "value_name": "0", "recent_item": "Progress_Report_Week3", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs\\.pdf"},
            {"category": ".docx", "value_name": "1", "recent_item": "Insider_Threat_Timeline", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs\\.docx"},
            {"category": ".xlsx", "value_name": "0", "recent_item": "USB_Evidence_Log", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs\\.xlsx"},
            {"category": "General", "value_name": "3", "recent_item": "NTUSER", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RecentDocs"},
        ]
        userassist = [
            {"guid": "{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}", "encoded_name": "Cebe.rgr", "decoded_name": "Pstd.exe", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}\\Count"},
            {"guid": "{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}", "encoded_name": "Purgrfg.rkr", "decoded_name": "Chrome.exe", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}\\Count"},
            {"guid": "{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}", "encoded_name": "PbaqLev.rkr", "decoded_name": "CmdLine.exe", "registry_path": "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}\\Count"},
        ]
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
