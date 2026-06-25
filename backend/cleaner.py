import logging
from datetime import datetime

def clean_pv_data(raw_data: dict) -> dict:
    """Cleans and structures raw PV data from the API."""
    if not raw_data:
        logging.error("No data to clean")
        return {}

    generation_w = 0.0
    consumption_w = 0.0

    for item in raw_data["data"]:
        if item["type"] == 'generation':
            generation_w += item["value"]
        elif item["type"] == "consumption":
            consumption_w += item["value"]

    timestamp = datetime.fromisoformat(raw_data["collected_at"])

    return {
        "timestamp": timestamp,
        "generation_w": generation_w,
        "consumption_w": consumption_w
    }