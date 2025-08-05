import unittest
import pandas as pd
from utils.input_validator import InputValidator

class TestInputValidator(unittest.TestCase):

    def setUp(self):
        # Sample mock dataframe
        data = {
            "date": pd.to_datetime(["2025-08-01", "2025-08-02", "2025-08-03"]),
            "room_type": ["Single", "Double", "Suite"],
            "available_rooms": [5, 3, 2],
        }
        self.df = pd.DataFrame(data)
        self.validator = InputValidator(self.df)

    def test_valid_input(self):
        valid, msg = self.validator.validate(
            dates=["2025-08-01", "2025-08-02"],
            room_type="Single",
            room_count=2
        )
        self.assertTrue(valid)
        self.assertIsNone(msg)

    def test_invalid_date_format(self):
        valid, msg = self.validator.validate(
            dates=["08-01-2025"],
            room_type="Double",
            room_count=1
        )
        self.assertFalse(valid)
        self.assertEqual(msg, "Invalid date format. Please use YYYY-MM-DD.")

    def test_date_not_available(self):
        valid, msg = self.validator.validate(
            dates=["2025-08-10"],  # Not in mock data
            room_type="Double",
            room_count=1
        )
        self.assertFalse(valid)
        self.assertEqual(msg, "No data available for date: 2025-08-10")

    def test_invalid_room_type(self):
        valid, msg = self.validator.validate(
            dates=["2025-08-01"],
            room_type="Presidential",  # Not in valid types
            room_count=1
        )
        self.assertFalse(valid)
        self.assertIn("Invalid room type.", msg)

    def test_invalid_room_count_zero(self):
        valid, msg = self.validator.validate(
            dates=["2025-08-01"],
            room_type="Single",
            room_count=0
        )
        self.assertFalse(valid)
        self.assertEqual(msg, "Room count must be an integer greater than zero.")

    def test_invalid_room_count_negative(self):
        valid, msg = self.validator.validate(
            dates=["2025-08-01"],
            room_type="Single",
            room_count=-1
        )
        self.assertFalse(valid)
        self.assertEqual(msg, "Room count must be an integer greater than zero.")

    def test_invalid_room_count_non_integer(self):
        valid, msg = self.validator.validate(
            dates=["2025-08-01"],
            room_type="Single",
            room_count="two"
        )
        self.assertFalse(valid)
        self.assertEqual(msg, "Room count must be an integer greater than zero.")

    def test_none_optional_fields(self):
        # Should succeed if date is valid and others are optional
        valid, msg = self.validator.validate(
            dates=["2025-08-01"],
            room_type=None,
            room_count=None
        )
        self.assertTrue(valid)
        self.assertIsNone(msg)

if __name__ == "__main__":
    unittest.main()
