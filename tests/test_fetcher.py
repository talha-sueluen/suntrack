import unittest
from unittest.mock import patch, MagicMock
from backend.fetcher import fetch_pv_data

class TestFetchPvData(unittest.TestCase):
    @patch("backend.fetcher.requests.get")
    def test_successful_fetch(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"collected_at": "2026-06-25T13:00:00+02:00", "data": [], "age_seconds": 1.0}
        mock_get.return_value = mock_response

        result = fetch_pv_data()

        self.assertIsInstance(result, dict)

    @patch("backend.fetcher.requests.get")
    def test_returns_empty_dict_on_error(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        result = fetch_pv_data()

        self.assertEqual(result, {})
if __name__ == "__main__":
    unittest.main()