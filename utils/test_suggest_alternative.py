import unittest
import pandas as pd
from suggest_alternative import (
    load_room_data,
    get_available_alternatives,
    suggest_cheaper_rooms
)

class TestSuggestAlternative(unittest.TestCase):

    def setUp(self):
        self.df = load_room_data()
    def test_available_alternatives(self):
        alt = get_available_alternatives(self.df, "2025-08-08", exclude_room_type="king")
        self.assertIn(("single", 5, 1000), alt)
        self.assertNotIn(("king", 0, 2000), alt)

    def test_cheaper_rooms(self):
        cheaper = suggest_cheaper_rooms(self.df, "2025-08-08", current_price=5000)
        self.assertIn(("single", 1000), cheaper)
        self.assertNotIn(("luxury", 5000), cheaper)

if __name__ == "__main__":
    unittest.main()
