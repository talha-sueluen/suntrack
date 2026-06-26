import requests
from dotenv import load_dotenv
import logging
import os

load_dotenv()


def fetch_pv_data() -> dict:
    """Fetches real-time PV data from API endpoint."""
    api_key = os.getenv("PV_API_KEY")
    url = os.getenv("PV_API_URL")
    if not api_key:
        logging.error("PV_API_KEY not found in environment variables")
        return {}
    headers = {"X-API-Key": api_key}
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to fetch PV data: {e}")
        return {}
