import logging
from datetime import datetime
from backend.storage import get_readings_for_day

def calculate_daily(date: datetime) -> dict:
    """Calculates daily generation and consumption totals."""
    readings = get_readings_for_day(date)
    if not readings:
        logging.warning("No readings found for the given day") # something is missing but code continues to work
        return {}

    total_generation = sum(float(r["generation_w"]) for r in readings)
    total_consumption = sum(float(r["consumption_w"]) for r in readings)
    pv_ratio = (total_generation / total_consumption * 100) if total_consumption > 0 else 0.0

    return {
        "date": date.strftime("%Y-%m-%d"),
        "total_generation_w": total_generation,
        "total_consumption_w": total_consumption,
        "pv_ratio_percent": round(pv_ratio, 2),
    }