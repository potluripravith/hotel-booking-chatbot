
import unittest
from unittest.mock import patch
from utils import fallback_utils

class TestFallbackUtils(unittest.TestCase):

    def test_is_irrelevant_input_true(self):
        user_input = "Tell me a joke"
        keywords = ["book", "availability", "price"]
        self.assertTrue(fallback_utils.is_irrelevant_input(user_input, keywords))

    def test_is_irrelevant_input_false(self):
        user_input = "Can I book a room for tomorrow?"
        keywords = ["book", "availability", "price"]
        self.assertFalse(fallback_utils.is_irrelevant_input(user_input, keywords))

    @patch("utils.fallback_utils.call_deepseek")
    def test_generate_ai_fallback(self, mock_call_deepseek):
        mock_call_deepseek.return_value = "Sure! Let's get back to your booking."
        result = fallback_utils.generate_ai_fallback("Tell me about aliens")
        self.assertEqual(result, "Sure! Let's get back to your booking.")
        mock_call_deepseek.assert_called_once()

if __name__ == "__main__":
    unittest.main()
