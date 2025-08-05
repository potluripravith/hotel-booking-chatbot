import unittest
import pandas as pd
from datetime import datetime

from utils.suggest_alternative import RoomAvailabilityService


class TestRoomAvailabilityService(unittest.TestCase):
    def setUp(self):
        # Sample room availability data
        self.test_data = pd.DataFrame({
            "date": pd.to_datetime([
                "2025-08-06", "2025-08-06", "2025-08-06",
                "2025-08-07", "2025-08-07"
            ]),
            "room_type": [
                "Deluxe", "Suite", "Standard",
                "Suite", "Standard"
            ],
            "available_rooms": [3, 0, 5, 2, 0],
            "price": [3000, 5000, 2000, 5000, 2000]
        })
        self.service = RoomAvailabilityService(data_source=self.test_data)

    def test_get_available_alternatives_with_rooms(self):
        result = self.service.get_available_alternatives("2025-08-06")
        expected = [("Deluxe", 3, 3000), ("Standard", 5, 2000)]
        self.assertEqual(result, expected)

    def test_get_available_alternatives_excluding_type(self):
        result = self.service.get_available_alternatives("2025-08-06", exclude_room_type="Deluxe")
        expected = [("Standard", 5, 2000)]
        self.assertEqual(result, expected)

    def test_get_available_alternatives_all_rooms_unavailable(self):
        result = self.service.get_available_alternatives("2025-08-07", exclude_room_type="Suite")
        expected = []  # Standard has 0 available
        self.assertEqual(result, expected)

    def test_get_available_alternatives_no_rooms_on_date(self):
        result = self.service.get_available_alternatives("2025-08-08")
        self.assertEqual(result, [])

    def test_suggest_cheaper_rooms_found(self):
        result = self.service.suggest_cheaper_rooms("2025-08-06", current_price=4000)
        expected = [("Deluxe", 3000), ("Standard", 2000)]
        self.assertEqual(result, expected)

    def test_suggest_cheaper_rooms_none_found(self):
        result = self.service.suggest_cheaper_rooms("2025-08-06", current_price=1500)
        self.assertEqual(result, [])

    def test_suggest_cheaper_rooms_all_unavailable(self):
        result = self.service.suggest_cheaper_rooms("2025-08-07", current_price=6000)
        expected = [("Suite", 5000)]  # Only Suite has rooms available
        self.assertEqual(result, expected)

    def test_suggest_cheaper_rooms_no_date_match(self):
        result = self.service.suggest_cheaper_rooms("2025-08-10", current_price=3000)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
