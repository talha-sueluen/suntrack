import unittest
from backend.cleaner import clean_pv_data


class TestCleanPvData(unittest.TestCase):

    def test_returns_empty_dict_on_empty_input(self):
        result = clean_pv_data({})
        self.assertEqual(result, {})

    def test_successful_clean(self):
        raw = {
            "collected_at": "2026-06-25T13:00:00+02:00",
            "data": [
                {"type": "generation", "value": 100.0},
                {"type": "consumption", "value": 200.0},
            ],
            "age_seconds": 1.0,
        }
        result = clean_pv_data(raw)
        self.assertIn("timestamp", result)
        self.assertIn("generation_w", result)
        self.assertIn("consumption_w", result)

    def test_correct_values(self):
        raw = {
            "collected_at": "2026-06-25T13:00:00+02:00",
            "data": [
                {"type": "generation", "value": 100.0},
                {"type": "generation", "value": 50.0},
                {"type": "consumption", "value": 200.0},
            ],
            "age_seconds": 1.0,
        }
        result = clean_pv_data(raw)
        self.assertEqual(result["generation_w"], 150.0)
        self.assertEqual(result["consumption_w"], 200.0)


if __name__ == "__main__":
    unittest.main()