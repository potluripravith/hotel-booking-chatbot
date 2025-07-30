import unittest
from utils.price_utils import load_room_data, extract_room_prices, get_price_for_room,calculate_total_price,calculate_combined_price

class TestPriceUtils(unittest.TestCase):

    def setUp(self):
        # Load real data from CSV
        self.df = load_room_data()
        self.price_map = extract_room_prices(self.df)

    def test_price_extraction(self):
        # Assuming these are the known fixed prices from your data
        expected = {
            'single': 1000,
            'king': 2000,
            'suite': 3000,
            'luxury': 5000
        }
        self.assertEqual(self.price_map, expected)

    def test_get_price_valid(self):
        self.assertEqual(get_price_for_room(self.price_map, 'suite'), 3000)
        self.assertEqual(get_price_for_room(self.price_map, 'king'), 2000)

    def test_get_price_invalid(self):
        self.assertIsNone(get_price_for_room(self.price_map, 'presidential'))
    def test_individual_price(self):
        total = calculate_total_price('king', nights=2, count=2, price_map=self.price_map)
        self.assertEqual(total, 8000)

    def test_combined_price(self):
        bookings = [
            ('king', 2, 2),    
            ('luxury', 1, 1)    
        ]
        total = calculate_combined_price(bookings, self.price_map)
        self.assertEqual(total, 13000)

    def test_invalid_room_type(self):
        bookings = [('presidential', 1, 1)]
        total = calculate_combined_price(bookings, self.price_map)
        self.assertEqual(total, 0)
    

if __name__ == '__main__':
    unittest.main()
