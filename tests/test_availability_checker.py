import unittest
import pandas as pd
from utils.availability_checker import AvailabilityChecker

class TestAvailabilityChecker(unittest.TestCase):
    def setUp(self):
        self.checker = AvailabilityChecker()
        self.sample_data = pd.DataFrame({
            "date": [
                pd.Timestamp("2025-08-01"), pd.Timestamp("2025-08-01"),
                pd.Timestamp("2025-08-02"), pd.Timestamp("2025-08-02")
            ],
            "room_type": ["Deluxe", "Suite", "Deluxe", "Suite"],
            "available_rooms": [2, 0, 3, 1]
        })

    # -------- check_single_date -------- #
    def test_single_date_no_room_type_or_count(self):
        date = pd.Timestamp("2025-08-01")
        df = self.sample_data[self.sample_data["date"] == date]
        result = self.checker.check_single_date(date, df, None, None)
        self.assertTrue(result[0])
        self.assertIsInstance(result[1], list)

    def test_single_date_only_room_type_available(self):
        date = pd.Timestamp("2025-08-02")
        df = self.sample_data[self.sample_data["date"] == date]
        result = self.checker.check_single_date(date, df, "Suite", None)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 1)

    def test_single_date_only_room_type_not_available(self):
        date = pd.Timestamp("2025-08-01")
        df = self.sample_data[self.sample_data["date"] == date]
        result = self.checker.check_single_date(date, df, "Suite", None)
        self.assertFalse(result[0])
        self.assertIn("not available", result[1])

    def test_single_date_only_room_count(self):
        date = pd.Timestamp("2025-08-02")
        df = self.sample_data[self.sample_data["date"] == date]
        result = self.checker.check_single_date(date, df, None, 2)
        self.assertTrue(result[0])
        self.assertIn("Deluxe", result[1])

    def test_single_date_room_type_and_count_sufficient(self):
        date = pd.Timestamp("2025-08-02")
        df = self.sample_data[self.sample_data["date"] == date]
        result = self.checker.check_single_date(date, df, "Deluxe", 2)
        self.assertTrue(result[0])
        self.assertEqual(result[1], "Available")

    def test_single_date_room_type_and_count_insufficient(self):
        date = pd.Timestamp("2025-08-01")
        df = self.sample_data[self.sample_data["date"] == date]
        result = self.checker.check_single_date(date, df, "Suite", 1)
        self.assertFalse(result[0])
        self.assertIn("not available", result[1])

    # -------- check_range_dates -------- #
    def test_range_dates_no_room_type_or_count(self):
        dates = [pd.Timestamp("2025-08-01"), pd.Timestamp("2025-08-02")]
        result = self.checker.check_range_dates(dates, self.sample_data, None, None)
        self.assertTrue(result[0])
        self.assertIn("Deluxe", result[1])

    def test_range_dates_only_room_type_available_all_dates(self):
        dates = [pd.Timestamp("2025-08-01"), pd.Timestamp("2025-08-02")]
        result = self.checker.check_range_dates(dates, self.sample_data, "Deluxe", None)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 2)



    def test_range_dates_only_room_count_all_dates_sufficient(self):
        dates = [pd.Timestamp("2025-08-01"), pd.Timestamp("2025-08-02")]
        result = self.checker.check_range_dates(dates, self.sample_data, None, 1)
        self.assertTrue(result[0])
        self.assertIsInstance(result[1], dict)

    def test_range_dates_room_count_insufficient_on_some_dates(self):
        dates = [pd.Timestamp("2025-08-01"), pd.Timestamp("2025-08-02")]
        result = self.checker.check_range_dates(dates, self.sample_data, None, 3)
        self.assertFalse(result[0])
        self.assertIn("No room type with at least 3 rooms", result[1])


    # -------- Edge cases -------- #
    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=["date", "room_type", "available_rooms"])
        date = pd.Timestamp("2025-08-01")
        result = self.checker.check_single_date(date, df, None, None)
        self.assertFalse(result[0])

    def test_invalid_room_type(self):
        date = pd.Timestamp("2025-08-01")
        df = self.sample_data[self.sample_data["date"] == date]
        result = self.checker.check_single_date(date, df, "Presidential", None)
        self.assertFalse(result[0])


if __name__ == '__main__':
    unittest.main()
