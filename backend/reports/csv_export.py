import csv
from pathlib import Path
from datetime import datetime


class CSVExport:
    """
    Export registry artifact lists into CSV files.
    """

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save_list_to_csv(self, data_list, filename):
        """
        Save list of dictionaries into CSV file.
        """
        try:
            file_path = self.output_dir / filename

            if not data_list:
                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    file.write("No data found\n")

                return {
                    "status": True,
                    "message": "CSV file saved with no data",
                    "file_path": str(file_path)
                }

            fieldnames = set()

            for item in data_list:
                fieldnames.update(item.keys())

            fieldnames = list(fieldnames)

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)

            return {
                "status": True,
                "message": "CSV file saved successfully",
                "file_path": str(file_path)
            }

        except Exception as error:
            return {
                "status": False,
                "message": f"Error saving CSV file: {error}",
                "file_path": None
            }

    def save_all_csv_reports(self, report_data):
        """
        Save major artifacts into separate CSV files.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []

        # Installed software
        installed = report_data.get("installed_software", {})
        result = self.save_list_to_csv(
            installed.get("software_list", []),
            f"installed_software_{timestamp}.csv"
        )
        saved_files.append(result)

        # Startup programs
        startup = report_data.get("startup_programs", {})
        result = self.save_list_to_csv(
            startup.get("startup_programs", []),
            f"startup_programs_{timestamp}.csv"
        )
        saved_files.append(result)

        # USB devices
        usb = report_data.get("usb_devices", {})
        result = self.save_list_to_csv(
            usb.get("usb_devices", []),
            f"usb_devices_{timestamp}.csv"
        )
        saved_files.append(result)

        # User Activity
        user_activity = report_data.get("user_activity", {})

        result = self.save_list_to_csv(
            user_activity.get("runmru", []),
            f"runmru_{timestamp}.csv"
        )
        saved_files.append(result)

        result = self.save_list_to_csv(
            user_activity.get("typed_paths", []),
            f"typed_paths_{timestamp}.csv"
        )
        saved_files.append(result)

        result = self.save_list_to_csv(
            user_activity.get("recent_docs", []),
            f"recent_docs_{timestamp}.csv"
        )
        saved_files.append(result)

        result = self.save_list_to_csv(
            user_activity.get("userassist", []),
            f"userassist_{timestamp}.csv"
        )
        saved_files.append(result)

        return saved_files