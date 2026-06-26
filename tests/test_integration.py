import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.fetcher import fetch_pv_data
from backend.cleaner import clean_pv_data
from backend.storage import init_storage, save_reading, get_readings_for_day
from backend.calculator import calculate_daily
import backend.storage as storage
import os

TEST_CSV = "test_integration.csv"


class TestIntegration(unittest.TestCase):

    def setUp(self):
        os.environ["PV_API_KEY"] = "test-key"
        os.environ["PV_API_URL"] = "https://test.url"
        storage.CSV_PATH = TEST_CSV
        init_storage()

    def tearDown(self):
        os.environ.pop("PV_API_KEY", None)
        os.environ.pop("PV_API_URL", None)
        if os.path.exists(TEST_CSV):
            os.remove(TEST_CSV)

    @patch("backend.fetcher.requests.get")
    def test_full_pipeline(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "collected_at": "2026-06-25T13:00:00+02:00",
            "data": [
                {"type": "generation", "value": 100.0},
                {"type": "consumption", "value": 200.0},
            ],
            "age_seconds": 1.0,
        }
        mock_get.return_value = mock_response

        raw = fetch_pv_data()
        data = clean_pv_data(raw)
        save_reading(data)
        result = calculate_daily(datetime(2026, 6, 25))

        self.assertIn("total_generation_w", result)
        self.assertEqual(result["total_generation_w"], 100.0)
        self.assertEqual(result["total_consumption_w"], 200.0)
        self.assertEqual(result["pv_ratio_percent"], 50.0)


if __name__ == "__main__":
    unittest.main()