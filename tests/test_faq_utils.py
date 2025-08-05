import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.faq_utils import FAQAnswerService

class TestFAQAnswerService(unittest.TestCase):

    @patch('utils.faq_utils.DataLoader')
    def setUp(self, mock_loader_class):
        # Create mock DataLoader instance
        mock_loader = MagicMock()
        mock_loader.load_faq_data.return_value = pd.DataFrame([
            {"question": "What is the check-in time?", "answer": "Check-in is from 2 PM."},
            {"question": "Do you allow pets?", "answer": "Yes, we are pet-friendly."}
        ])
        mock_loader_class.return_value = mock_loader

        self.service = FAQAnswerService(threshold=50)

    def test_exact_match(self):
        question = "What is the check-in time?"
        answer = self.service.get_answer(question)
        self.assertIn("2 PM", answer)

    def test_fuzzy_match(self):
        question = "When can I check in?"
        answer = self.service.get_answer(question)
        self.assertIn("2 PM", answer)

    def test_no_match(self):
        question = "Is there a helipad on the roof?"
        answer = self.service.get_answer(question)
        self.assertIn("couldn't find", answer)

if __name__ == '__main__':
    unittest.main()
