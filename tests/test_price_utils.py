import unittest
from unittest.mock import patch
import pandas as pd
from utils.price_utils import PriceCalculator

class TestPriceCalculator(unittest.TestCase):

    @patch("utils.price_utils.DataLoader")
    def setUp(self, mock_loader_class):
        mock_loader = mock_loader_class.return_value
        mock_loader.load_room_data.return_value = pd.DataFrame([
            {"date": "2025-08-05", "room_type": "Single", "price": 100},
            {"date": "2025-08-06", "room_type": "Single", "price": 100},
            {"date": "2025-08-05", "room_type": "Double", "price": 150},
            {"date": "2025-08-06", "room_type": "Double", "price": 150}
        ])
        self.calculator = PriceCalculator()

    def test_extract_room_prices(self):
        expected = {"Single": 100, "Double": 150}
        self.assertEqual(self.calculator.room_prices, expected)

    def test_get_price_for_valid_room_type(self):
        self.assertEqual(self.calculator.get_price_for_room("Single"), 100)
        self.assertEqual(self.calculator.get_price_for_room("Double"), 150)

    def test_get_price_for_invalid_room_type(self):
        self.assertIsNone(self.calculator.get_price_for_room("Suite"))

    def test_calculate_total_price_valid(self):
        self.assertEqual(self.calculator.calculate_total_price("Single", 2, 3), 600)

    def test_calculate_total_price_invalid_room(self):
        self.assertEqual(self.calculator.calculate_total_price("Suite", 2, 3), 0)

    def test_calculate_total_price_zero_nights(self):
        self.assertEqual(self.calculator.calculate_total_price("Single", 0, 2), 0)

    def test_calculate_total_price_zero_count(self):
        self.assertEqual(self.calculator.calculate_total_price("Single", 2, 0), 0)

    def test_calculate_combined_price_multiple_bookings(self):
        bookings = [("Single", 2, 2), ("Double", 1, 1)]  # 2*2*100 + 1*1*150 = 400 + 150 = 550
        self.assertEqual(self.calculator.calculate_combined_price(bookings), 550)

    def test_calculate_combined_price_empty_list(self):
        self.assertEqual(self.calculator.calculate_combined_price([]), 0)

    def test_calculate_combined_price_with_invalid_room_type(self):
        bookings = [("Single", 2, 2), ("Suite", 3, 1)]  # Suite not in list
        self.assertEqual(self.calculator.calculate_combined_price(bookings), 400)

if __name__ == "__main__":
    unittest.main()
