import unittest
import pandas as pd
from datetime import datetime

from booking_utils import check_availability, normalize_date, load_room_data


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


class TestCheckAvailability(unittest.TestCase):
    def setUp(self):
        self.df = load_room_data()

    def test_single_date_only(self):
        result, data = check_availability(["2025-08-01"])
        self.assertTrue(result)
        self.assertTrue(any(r["available_rooms"] > 0 for r in data))
    def test_single_date_only(self):
        result, msg = check_availability(["2025-08-11"])
        self.assertFalse(result)
        self.assertIn("No rooms",msg)

    def test_single_date_with_room_type(self):
        result, data = check_availability(["2025-08-01"], room_type="single")
        self.assertTrue(result)
        self.assertEqual(data, 5)

    def test_single_date_with_room_type_unavailable(self):
        result, msg = check_availability(["2025-08-01"], room_type="suite")
        self.assertFalse(result)
        self.assertIn("not available", msg)

    def test_single_date_with_room_count(self):
        result, data = check_availability(["2025-08-01"], room_count=2)
        self.assertTrue(result)
        self.assertIn("single", data)

    def test_single_date_with_room_type_and_count_valid(self):
        result, msg = check_availability(["2025-08-01"], room_type="king", room_count=2)
        self.assertTrue(result)

    def test_single_date_with_room_type_and_count_unavailable(self):
        result, msg = check_availability(["2025-08-01"], room_type="king", room_count=4)
        self.assertFalse(result)
        self.assertIn("not available", msg)

    def test_single_date_with_zero_count(self):
        result, msg = check_availability(["2025-08-01"], room_type="single", room_count=0)
        self.assertFalse(result)
        self.assertIn("Room count must be an integer greater than zero", msg)

    def test_range_dates_common_room_types(self):
        dates = normalize_date("August 5-7, 2025", datetime(2025, 7, 29))
        result, data = check_availability(dates)
        self.assertTrue(result)
        self.assertIn("king", data)
        self.assertGreaterEqual(data["king"], 1)
    def test_range_dates_common_room_types(self):
        dates = normalize_date("August 8-11, 2025", datetime(2025, 7, 29))
        result, msg = check_availability(dates)
        self.assertFalse(result)
        self.assertIn("No common room",msg)
    def test_range_dates_no_common_room_type(self):
        dates = normalize_date("August 1-3, 2025", datetime(2025, 7, 29))
        result, msg = check_availability(dates)
        self.assertTrue(result)
        self.assertIn("luxury", msg)

    def test_range_with_room_type_available_all_days(self):
        dates = normalize_date("August 2-4, 2025", datetime(2025, 7, 29))
        result, min_available = check_availability(dates, room_type="suite")
        self.assertTrue(result)
        self.assertEqual(min_available, 2)  # min across Aug 2,3,4 is 2

    def test_range_with_room_type_unavailable_one_day(self):
        dates = normalize_date("August 1-3, 2025", datetime(2025, 7, 29))
        result, msg = check_availability(dates, room_type="suite")
        self.assertFalse(result)
        self.assertIn("not available", msg)

    def test_range_with_room_count_and_no_type(self):
        dates = normalize_date("August 5-7, 2025", datetime(2025, 7, 29))
        result, data = check_availability(dates, room_count=2)
        self.assertFalse(result)
        self.assertIn("No room type with at least 2 rooms on 2025-08-06", data)

    def test_range_with_room_count_insufficient(self):
        dates = normalize_date("August 2-3, 2025", datetime(2025, 7, 29))
        result, msg = check_availability(dates, room_count=5)
        self.assertFalse(result)
        self.assertIn("No room type", msg)

    def test_range_with_room_count_and_type_available(self):
        dates = normalize_date("August 2-4, 2025", datetime(2025, 7, 29))
        result, msg = check_availability(dates, room_type="suite", room_count=2)
        self.assertTrue(result)

    def test_range_with_room_count_and_type_unavailable(self):
        dates = normalize_date("August 1-3, 2025", datetime(2025, 7, 29))
        result, msg = check_availability(dates, room_type="suite", room_count=2)
        self.assertFalse(result)
        self.assertIn("not available", msg)

    def test_zero_room_count_in_range(self):
        dates = normalize_date("August 5-7, 2025", datetime(2025, 7, 29))
        result, msg = check_availability(dates, room_count=0)
        self.assertFalse(result)
        self.assertIn("Room count must be an integer greater than zero", msg)

    def test_date_not_in_data(self):
        result, msg = check_availability(["2025-09-01"])
        self.assertFalse(result)
        self.assertIn("No data", msg)
    def test_weekend_suite_availability(self):
        dates = normalize_date("this weekend", datetime(2025, 7, 29))  # ['2025-08-09', '2025-08-10']
        result, msg = check_availability(dates, room_type="suite", room_count=1)
        self.assertTrue(result)
        self.assertEqual(msg, "Available")
    def test_date_not_in_data(self):
        result, msg = check_availability(["2025-09-01"])
        self.assertFalse(result)
        self.assertIn("No data", msg)


if __name__ == "__main__":
    unittest.main()


    
    
