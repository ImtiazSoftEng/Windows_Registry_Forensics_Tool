import csv
from pathlib import Path
from datetime import datetime


class CSVExport:
    """
    Export registry artifact data into CSV files.
    """

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def get_fieldnames(self, data_list):
        """
        Get all field names from list of dictionaries.
        """
        fieldnames = []

        for item in data_list:
            for key in item.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

        return fieldnames

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
                    "message": "CSV saved with no data",
                    "file_path": str(file_path)
                }

            fieldnames = self.get_fieldnames(data_list)

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(data_list)

            return {
                "status": True,
                "message": "CSV saved successfully",
                "file_path": str(file_path)
            }

        except Exception as error:
            return {
                "status": False,
                "message": f"Error saving CSV: {error}",
                "file_path": None
            }

    def save_dict_to_csv(self, data_dict, filename):
        """
        Save simple dictionary into CSV file.
        Good for system info summary.
        """
        try:
            file_path = self.output_dir / filename

            rows = []

            for key, value in data_dict.items():
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        rows.append({
                            "field": f"{key}.{sub_key}",
                            "value": sub_value
                        })
                else:
                    rows.append({
                        "field": key,
                        "value": value
                    })

            return self.save_list_to_csv(rows, filename)

        except Exception as error:
            return {
                "status": False,
                "message": f"Error saving dictionary CSV: {error}",
                "file_path": None
            }

    def save_all_csv_reports(self, report_data):
        """
        Save all important artifacts into separate CSV files.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = []

        # 1. System Info
        system_info = report_data.get("system_info", {})
        saved_files.append(
            self.save_dict_to_csv(
                system_info,
                f"system_info_{timestamp}.csv"
            )
        )

        # 2. Installed Software
        installed = report_data.get("installed_software", {})
        saved_files.append(
            self.save_list_to_csv(
                installed.get("software_list", []),
                f"installed_software_{timestamp}.csv"
            )
        )

        # 3. Startup Programs
        startup = report_data.get("startup_programs", {})
        saved_files.append(
            self.save_list_to_csv(
                startup.get("startup_programs", []),
                f"startup_programs_{timestamp}.csv"
            )
        )

        # 4. USB Devices
        usb = report_data.get("usb_devices", {})
        saved_files.append(
            self.save_list_to_csv(
                usb.get("usb_devices", []),
                f"usb_devices_{timestamp}.csv"
            )
        )

        # 5. User Activity
        user_activity = report_data.get("user_activity", {})

        saved_files.append(
            self.save_list_to_csv(
                user_activity.get("runmru", []),
                f"runmru_{timestamp}.csv"
            )
        )

        saved_files.append(
            self.save_list_to_csv(
                user_activity.get("typed_paths", []),
                f"typed_paths_{timestamp}.csv"
            )
        )

        saved_files.append(
            self.save_list_to_csv(
                user_activity.get("recent_docs", []),
                f"recent_docs_{timestamp}.csv"
            )
        )

        saved_files.append(
            self.save_list_to_csv(
                user_activity.get("userassist", []),
                f"userassist_{timestamp}.csv"
            )
        )

        return saved_files