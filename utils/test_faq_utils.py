import unittest
from faq_utils import load_faq_data, get_faq_answer

class TestFAQUtils(unittest.TestCase):
    def setUp(self):
        self.faq_df = load_faq_data()

    def test_exact_match(self):
        question = "What time is check-in?"
        answer = get_faq_answer(question, self.faq_df)
        self.assertIn("2 PM", answer)

    def test_fuzzy_match(self):
        question = "When can I check in?"
        answer = get_faq_answer(question, self.faq_df)
        self.assertIn("2 PM", answer)

    def test_no_match(self):
        question = "Is there a helipad on the roof?"  # something absurd
        answer = get_faq_answer(question, self.faq_df)
        self.assertIn("Sorry, I couldn't find an answer to that question", answer)
if __name__ == '__main__':
    unittest.main()
