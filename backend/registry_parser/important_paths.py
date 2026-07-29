"""
Important Registry Paths
Member 1 will use these paths to read useful forensic registry artifacts.
"""

NTUSER_PATHS = {
    "RunMRU": r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU",
    "RecentDocs": r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs",
    "TypedPaths": r"Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths",
    "UserAssist": r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist",
    "UserStartup": r"Software\Microsoft\Windows\CurrentVersion\Run",
}

SYSTEM_PATHS = {
    "USBSTOR": r"ControlSet001\Enum\USBSTOR",
    "MountedDevices": r"MountedDevices",
    "ComputerName": r"ControlSet001\Control\ComputerName\ComputerName",
    "TimeZone": r"ControlSet001\Control\TimeZoneInformation",
}

SOFTWARE_PATHS = {
    "InstalledPrograms": r"Microsoft\Windows\CurrentVersion\Uninstall",
    "StartupPrograms": r"Microsoft\Windows\CurrentVersion\Run",
    "WindowsVersion": r"Microsoft\Windows NT\CurrentVersion",
}