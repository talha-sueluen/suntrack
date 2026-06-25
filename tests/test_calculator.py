import unittest
from unittest.mock import patch
from datetime import datetime
from backend.calculator import calculate_daily


class TestCalculateDaily(unittest.TestCase):

    @patch("backend.calculator.get_readings_for_day")
    def test_successful_calculation(self, mock_readings):
        mock_readings.return_value = [
            {"generation_w": "100.0", "consumption_w": "200.0"},
            {"generation_w": "50.0", "consumption_w": "100.0"},
        ]
        result = calculate_daily(datetime(2026, 6, 25))
        self.assertEqual(result["total_generation_w"], 150.0)
        self.assertEqual(result["total_consumption_w"], 300.0)
        self.assertEqual(result["pv_ratio_percent"], 50.0)

    @patch("backend.calculator.get_readings_for_day")
    def test_empty_readings(self, mock_readings):
        mock_readings.return_value = []
        result = calculate_daily(datetime(2026, 6, 25))
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()