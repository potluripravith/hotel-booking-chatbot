import unittest
import pandas as pd
from datetime import datetime
from booking_utils import load_room_data,normalize_date

class TestBookingUtils(unittest.TestCase):

    def test_load_room_data_exists(self):
        try:
            df = load_room_data()  # default path used
            self.assertIsInstance(df, pd.DataFrame)
        except FileNotFoundError:
            self.fail("CSV file not found. Ensure 'knowledge_base/room_availability.csv' exists.")
        except Exception as e:
            self.fail(f"Unexpected error occurred: {e}")
from datetime import datetime
print(normalize_date("August 15, 2025", datetime(2025, 7, 29)))

class TestNormalizeDate(unittest.TestCase):
    def setUp(self):
        self.base_date = datetime(2025, 7, 29)  # Tuesday, July 29, 2025

    def test_relative_dates(self):
        self.assertEqual(normalize_date("today", self.base_date), ["2025-07-29"])
        self.assertEqual(normalize_date("tomorrow", self.base_date), ["2025-07-30"])
        self.assertEqual(normalize_date("next friday", self.base_date), ["2025-08-08"])
        self.assertEqual(normalize_date("yesterday", self.base_date), ["2025-07-28"])

    def test_absolute_dates(self):
        self.assertEqual(normalize_date("August 15, 2025", self.base_date), ["2025-08-15"])
        self.assertEqual(normalize_date("15th August", self.base_date), ["2025-08-15"])
        self.assertEqual(normalize_date("2025-12-31", self.base_date), ["2025-12-31"])
        self.assertEqual(normalize_date("Jan 1 2026", self.base_date), ["2026-01-01"])

    def test_date_ranges(self):
        self.assertEqual(
            normalize_date("this weekend", self.base_date),
            ["2025-08-02", "2025-08-03"]
        )
        self.assertEqual(
            normalize_date("August 1-3, 2025", self.base_date),
            ["2025-08-01", "2025-08-02", "2025-08-03"]
        )
        self.assertEqual(
            normalize_date("next week", self.base_date),
            ["2025-08-04", "2025-08-05", "2025-08-06", "2025-08-07",
             "2025-08-08", "2025-08-09", "2025-08-10"]
        )

if __name__ == "__main__":
    unittest.main()