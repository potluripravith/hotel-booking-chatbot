import unittest
from unittest.mock import patch
from llm import extract_booking_info

class TestExtractFunction(unittest.TestCase):
    
    @patch("llm.call_deepseek")
    def test_full_information(self, mock_call):
        mock_call.return_value = {
            "dates": ["2025-08-01", "2025-08-02"],
            "room_type": "deluxe",
            "room_count": 2,
        }
        result = extract_booking_info("I want to book 2 deluxe rooms on August 1 and 2.")
        self.assertEqual(result["room_type"], "deluxe")
        self.assertEqual(result["dates"], ["2025-08-01", "2025-08-02"])
        self.assertEqual(result["room_count"], 2)

    @patch("llm.call_deepseek")
    def test_only_date(self, mock_call):
        mock_call.return_value = {
            "dates": ["2025-08-05"],
            "room_type": None,
            "room_count": None,
\
        }
        result = extract_booking_info("I need a room for August 5th.")
        self.assertEqual(result["dates"], ["2025-08-05"])
        self.assertIsNone(result["room_type"])

    @patch("llm.call_deepseek")
    def test_only_room_type(self, mock_call):
        mock_call.return_value = {
            "dates": [],
            "room_type": "deluxe",
            "room_count": None,
\
        }
        result = extract_booking_info("Show me deluxe rooms.")
        self.assertEqual(result["room_type"], "deluxe")
        self.assertEqual(result["dates"], [])

    @patch("llm.call_deepseek")
    def test_empty_input(self, mock_call):
        mock_call.return_value = {}
        result = extract_booking_info("")
        self.assertEqual(result["dates"], [])
        self.assertIsNone(result["room_type"])
        self.assertIsNone(result["room_count"])


if __name__ == "__main__":
    unittest.main()
