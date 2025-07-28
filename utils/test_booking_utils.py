import unittest
from datetime import datetime, timedelta
# import parsedatetime as pdt
import pandas as pd
from booking_utils import normalize_date, check_availability  # Assuming the code is in booking_utils.py

class TestNormalizeDate(unittest.TestCase):
    def setUp(self):
        self.base_date = datetime(2025, 7, 29)  # Tuesday, July 29, 2025 (as per context)

    def test_relative_dates(self):
        # Test today
        self.assertEqual(normalize_date("today", self.base_date), ["2025-07-29"])
        # Test tomorrow
        self.assertEqual(normalize_date("tomorrow", self.base_date), ["2025-07-30"])
        # Test next friday (from Tuesday: Friday is Aug 1)
        self.assertEqual(normalize_date("next friday", self.base_date), ["2025-08-01"])
        # Test next month (August 29)
        self.assertEqual(normalize_date("next month", self.base_date), ["2025-08-29"])
        # Test yesterday
        self.assertEqual(normalize_date("yesterday", self.base_date), ["2025-07-28"])

    def test_absolute_dates(self):
        # Test specific date formats
        self.assertEqual(normalize_date("August 15, 2025", self.base_date), ["2025-08-15"])
        self.assertEqual(normalize_date("15th August", self.base_date), ["2025-08-15"])
        self.assertEqual(normalize_date("2025-12-31", self.base_date), ["2025-12-31"])
        self.assertEqual(normalize_date("Jan 1 2026", self.base_date), ["2026-01-01"])

    def test_date_ranges(self):
        # Test weekend range
        self.assertEqual(
            normalize_date("this weekend", self.base_date),
            ["2025-08-02", "2025-08-03"]  # Saturday and Sunday
        )
        # Test date range with hyphen
        self.assertEqual(
            normalize_date("August 1-3, 2025", self.base_date),
            ["2025-08-01", "2025-08-02", "2025-08-03"]
        )
        # Test "next week" (should return full week)
        self.assertEqual(
            normalize_date("next week", self.base_date),
            [f"2025-08-{d}" for d in range(4, 10)]  # Mon-Sun next week
        )


class TestCheckAvailability(unittest.TestCase):
    def setUp(self):
        # Create mock room availability data
        data = {
            'date': ['2025-07-29', '2025-07-29', '2025-07-30', '2025-07-30', '2025-08-01'],
            'room_type': ['Deluxe', 'Suite', 'Deluxe', 'Suite', 'Deluxe'],
            'available_rooms': [5, 0, 3, 2, 4]
        }
        self.df = pd.DataFrame(data)

    def test_single_date_sufficient(self):
        # Sufficient Deluxe rooms on 2025-07-29
        result = check_availability(self.df, "2025-07-29", "Deluxe", 3)
        self.assertEqual(result, "5 Deluxe room(s) available")

    def test_single_date_insufficient(self):
        # Only 2 Suite rooms available when needing 3
        result = check_availability(self.df, "2025-07-30", "Suite", 3)
        self.assertEqual(result, "Only 2 Suite room(s) available, need 3")

    def test_single_date_no_rooms(self):
        # Suite unavailable on 2025-07-29
        result = check_availability(self.df, "2025-07-29", "Suite", 1)
        self.assertEqual(result, "Suite not available")

    def test_single_date_no_data(self):
        # Date not in DataFrame
        result = check_availability(self.df, "2025-12-25", "Deluxe")
        self.assertEqual(result, "No data available")

    def test_multi_date(self):
        # Check multiple dates without room type
        dates = ["2025-07-29", "2025-07-30", "2025-08-01"]
        expected = {
            "2025-07-29": {"Deluxe": "5 room(s) available"},
            "2025-07-30": {"Deluxe": "3 room(s) available", "Suite": "2 room(s) available"},
            "2025-08-01": {"Deluxe": "4 room(s) available"}
        }
        result = check_availability(self.df, dates)
        self.assertDictEqual(result, expected)

    def test_no_room_type_single_date(self):
        # All available rooms for single date
        result = check_availability(self.df, "2025-07-29")
        self.assertDictEqual(result, {"Deluxe": "5 room(s) available"})

    def test_zero_count(self):
        # Edge case: 0 rooms requested
        result = check_availability(self.df, "2025-07-29", "Deluxe", 0)
        self.assertEqual(result, "5 Deluxe room(s) available")

    def test_all_room_types_unavailable(self):
        # Date where all room types are unavailable
        result = check_availability(self.df, "2025-07-29", "Suite")
        self.assertEqual(result, "Suite not available")

if __name__ == '__main__':
    unittest.main()