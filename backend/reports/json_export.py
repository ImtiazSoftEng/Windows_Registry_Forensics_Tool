import json
from pathlib import Path
from datetime import datetime


class JSONExport:
    """
    Export full registry scan data into JSON file.
    """

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save_json(self, data, filename=None):
        """
        Save dictionary data into JSON file.
        """
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"registry_scan_report_{timestamp}.json"

            file_path = self.output_dir / filename

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False, default=str)

            return {
                "status": True,
                "message": "JSON report saved successfully",
                "file_path": str(file_path)
            }

        except Exception as error:
            return {
                "status": False,
                "message": f"Error saving JSON report: {error}",
                "file_path": None
            }