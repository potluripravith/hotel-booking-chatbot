import unittest
from utils.routing import route_from_input

class TestRouting(unittest.TestCase):

    def test_route_booking(self):
        state = {"user_input": "I want to book a room"}
        self.assertEqual(route_from_input(state), "booking_node")

    def test_route_faq(self):
        state = {"user_input": "Do you have Wi-Fi?"}
        self.assertEqual(route_from_input(state), "faq_node")

    def test_route_price(self):
        state = {"user_input": "How much is a double room?"}
        self.assertEqual(route_from_input(state), "price_node")

    def test_route_fallback(self):
        state = {"user_input": "Tell me a joke"}
        self.assertEqual(route_from_input(state), "fallback_node")

if __name__ == '__main__':
    unittest.main()