import unittest
import os   # to talk with operating system
from datetime import datetime
from backend.storage import init_storage, save_reading, get_readings_for_day

TEST_CSV = "test_suntrack.csv"

class TestStorage(unittest.TestCase):

    def setUp(self):
        import backend.storage as storage
        storage.CSV_PATH = TEST_CSV
        init_storage()

    def tearDown(self):
        if os.path.exists(TEST_CSV):
            os.remove(TEST_CSV)

    def test_init_creates_file(self):
        self.assertTrue(os.path.exists(TEST_CSV))

    def test_save_reading(self):
        data = {
            "timestamp": datetime(2026, 6, 25, 13, 0, 0),
            "generation_w": 100.0,
            "consumption_w": 200.0,
        }
        save_reading(data)
        rows = get_readings_for_day(datetime(2026, 6, 25))
        self.assertEqual(len(rows), 1)

    def test_save_empty_data(self):
        save_reading({})
        rows = get_readings_for_day(datetime(2026, 6, 25))
        self.assertEqual(len(rows), 0)

if __name__ == "__main__":
    unittest.main()