
import platform
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory, abort

from backend.reports.json_export import JSONExport
from backend.reports.csv_export import CSVExport

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    from backend.live_registry.system_info import SystemInfoReader
    from backend.live_registry.installed_software import InstalledSoftwareReader
    from backend.live_registry.startup_programs import StartupProgramsReader
    from backend.live_registry.usb_devices import USBDevicesReader
    from backend.live_registry.user_activity import UserActivityReader
else:
    from backend.mock.mock_readers import (
        SystemInfoReader,
        InstalledSoftwareReader,
        StartupProgramsReader,
        USBDevicesReader,
        UserActivityReader,
    )

OUTPUT_DIR = Path("output")

app = Flask(__name__)


# ---------------------------------------------------------------- #
# Page
# ---------------------------------------------------------------- #

@app.route("/")
def index():
    return render_template("index.html", mode="windows" if IS_WINDOWS else "dev")


# ---------------------------------------------------------------- #
# Per-artifact API — mirrors main.py's print_*() functions, but
# returns JSON instead of printing to a terminal.
# ---------------------------------------------------------------- #

@app.route("/api/system-info")
def api_system_info():
    return jsonify(SystemInfoReader().get_system_info())


@app.route("/api/installed-software")
def api_installed_software():
    return jsonify(InstalledSoftwareReader().get_installed_software())


@app.route("/api/startup-programs")
def api_startup_programs():
    return jsonify(StartupProgramsReader().get_startup_programs())


@app.route("/api/usb-devices")
def api_usb_devices():
    return jsonify(USBDevicesReader().read_usb_devices())


@app.route("/api/user-activity")
def api_user_activity():
    return jsonify(UserActivityReader().get_user_activity())


# ---------------------------------------------------------------- #
# Full scan — mirrors main.py's generate_full_report()
# ---------------------------------------------------------------- #

@app.route("/api/scan/full", methods=["POST"])
def api_scan_full():
    system_info = SystemInfoReader().get_system_info()
    installed_software = InstalledSoftwareReader().get_installed_software()
    startup_programs = StartupProgramsReader().get_startup_programs()
    usb_devices = USBDevicesReader().read_usb_devices()
    user_activity = UserActivityReader().get_user_activity()

    report_data = {
        "tool_name": "Portable Windows Registry Forensic Analyzer",
        "tool_mode": "Live Registry Analysis" if IS_WINDOWS else "Dev / Mock Mode",
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_info": system_info,
        "installed_software": installed_software,
        "startup_programs": startup_programs,
        "usb_devices": usb_devices,
        "user_activity": user_activity,
    }

    json_result = JSONExport(output_dir=str(OUTPUT_DIR)).save_json(report_data)
    csv_results = CSVExport(output_dir=str(OUTPUT_DIR)).save_all_csv_reports(report_data)

    return jsonify({
        "report": report_data,
        "json_export": json_result,
        "csv_exports": csv_results,
    })


# ---------------------------------------------------------------- #
# Download a previously saved report file from output/
# ---------------------------------------------------------------- #

@app.route("/api/export/download/<path:filename>")
def api_download_report(filename):
    if not (OUTPUT_DIR / filename).exists():
        abort(404, description="Report file not found.")
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
