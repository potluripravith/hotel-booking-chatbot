import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from rapidfuzz import fuzz, process
from utils.load_data import DataLoader


STOP_WORDS = set(stopwords.words("english"))


class FAQAnswerService:
    def __init__(self, scorer=fuzz.token_sort_ratio, threshold: int = 55):
        """
        Initializes the FAQAnswerService by loading data and precomputing cleaned questions.
        """
        self.scorer = scorer
        self.threshold = threshold
        loader = DataLoader()
        self.faq_df = loader.load_faq_data()  
        self._validate_columns()
        self.cleaned_questions = self.faq_df["question"].apply(self.clean_text)

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans input text by lowercasing, removing punctuation, tokenizing,
        and filtering out stopwords.
        """
        text = text.lower()
        text = re.sub(f"[{string.punctuation}]", "", text)
        tokens = word_tokenize(text)
        return " ".join([w for w in tokens if w not in STOP_WORDS])

    def _validate_columns(self):
        """
        Ensures the required 'question' and 'answer' columns exist.
        """
        required_cols = {"question", "answer"}
        if not required_cols.issubset(self.faq_df.columns):
            raise ValueError("FAQ data must contain 'question' and 'answer' columns.")

    def get_answer(self, user_question: str) -> str:
        """
        Returns the most relevant answer for the given user question.
        """
        cleaned_input = self.clean_text(user_question)
        match = process.extractOne(cleaned_input, self.cleaned_questions, scorer=self.scorer)

        if match and match[1] >= self.threshold:
            _, _, index = match
            return self.faq_df.loc[index, "answer"]

        return "Sorry, I couldn't find an answer to that question."
