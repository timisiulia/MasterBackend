import csv
import os
from datetime import datetime

class ShollCSVLogger:
    def __init__(self, csv_path="outputs/sholl_results.csv"):
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

        # Creează fișierul CSV dacă nu există deja
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Image Name",
                    "ROI Index",
                    "ROI Folder",
                    "ROI Height (px)",
                    "ROI Width (px)",
                    "Binary Area (pixels)",
                    "Max Intersections",
                    "Total Intersections",
                    "Timestamp"
                ])

    def log_result(self, image_name: str, roi_index: int, roi_folder: str,
                   roi_shape: tuple, binary_area: int,
                   max_intersections: int, total_intersections: int):
        height, width = roi_shape
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                image_name,
                roi_index,
                roi_folder,
                height,
                width,
                binary_area,
                max_intersections,
                total_intersections,
                timestamp
            ])
