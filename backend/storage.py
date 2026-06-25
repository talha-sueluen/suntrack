import csv
import logging
import os
from datetime import datetime

CSV_PATH = "suntrack.csv"

def init_storage():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f: #w = write mode # when block is finished, calls f.close() automatic
            writer = csv.writer(f)
            writer.writerow(["timestamp", "generation_w", "consumption_w"])

def save_reading(data: dict):
    """Saves a cleaned PV reading to the CSV file."""
    if not data:
        logging.error("No data to save")
        return
    try:
        with open(CSV_PATH, "a", newline="") as f:  #a = append mode
            writer = csv.writer(f)
            writer.writerow([
                data["timestamp"].isoformat(),
                data["generation_w"],
                data["consumption_w"],
            ])
    except Exception as e:
        logging.error(f"Failed to save reading: {e}")

def get_readings_for_day(date: datetime) -> list:
    """Returns all readings for a given day."""
    try:
        day_str = date.strftime("%Y-%m-%d")   #YYYY-MM-DD
        with open(CSV_PATH, "r") as f:
            reader = csv.DictReader(f)
            return [row for row in reader
                    if row["timestamp"].startswith(day_str)]
    except Exception as e:
        logging.error(f"Failed to get readings: {e}")
        return []