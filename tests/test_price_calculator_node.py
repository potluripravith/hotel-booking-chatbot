import unittest
from state import State
from nodes.price_calculation import price_calculation_node

class TestPriceCalculationNode(unittest.TestCase):

    def test_valid_price_calculation(self):
        state = State()
        state["room_type"] = "king"
        state["room_count"] = 2
        state["dates"] = ["2025-08-01", "2025-08-02"]  # 2 nights

        updated_state = price_calculation_node(state)

        # Replace ₹2000 with actual price of "king" room from your data if different
        expected_price = 2 * 2000 * 2
        self.assertEqual(updated_state["total_price"], expected_price)
        self.assertIn("total price is ₹8000", updated_state["agent_message"])

    def test_unavailable_room_type(self):
        state = State()
        state["room_type"] = "nonexistent"
        state["room_count"] = 1
        state["dates"] = ["2025-08-01", "2025-08-02"]

        updated_state = price_calculation_node(state)
        self.assertIn("couldn't calculate the price", updated_state["agent_message"])
        self.assertEqual(updated_state.get("total_price", 0), 0)

    def test_missing_booking_details(self):
        state = State()
        state["room_type"] = "king"
        # Missing room_count and dates

        updated_state = price_calculation_node(state)
        self.assertIn("Booking details are incomplete", updated_state["agent_message"])
        self.assertNotIn("total_price", updated_state)

if __name__ == "__main__":
    unittest.main()
