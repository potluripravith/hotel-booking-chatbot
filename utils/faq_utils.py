import pandas as pd
from rapidfuzz import fuzz, process
import os
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.data import find

def ensure_nltk_resources():
    """Ensures that necessary NLTK resources ('punkt' and 'stopwords') are available and Downloads them if not already present"""
    for resource_id, resource_name in [("tokenizers/punkt", "punkt"), ("corpora/stopwords", "stopwords")]:
        try:
            find(resource_id)
        except LookupError:
            nltk.download(resource_name)

ensure_nltk_resources()

STOP_WORDS = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """Cleans input text by lowercasing, removing punctuation, tokenizing and filtering out English stopwords."""
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in STOP_WORDS]
    return " ".join(filtered_tokens)

def load_faq_data()-> pd.DataFrame:
    """Loads FAQ data from a CSV file located in the 'knowledge_base' directory"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, '..', 'knowledge_base', 'Hotel_faqs.csv')
    return pd.read_csv(path)

def get_faq_answer(user_question: str, faq_df: pd.DataFrame) -> str:
    """Finds the most relevant FAQ answer to the user's question using fuzzy string matching"""
    if "question" not in faq_df.columns or "answer" not in faq_df.columns:
        raise ValueError("FAQ CSV must contain 'question' and 'answer' columns.")
    cleaned_user_question = clean_text(user_question)

    cleaned_questions = faq_df["question"].apply(clean_text)
    match = process.extractOne(
    cleaned_user_question,
    cleaned_questions,
    scorer=fuzz.token_sort_ratio
    )
    FUZZY_MATCH_THRESHOLD = 55
    if match and match[1] >= FUZZY_MATCH_THRESHOLD:
        _, _, index = match
        return faq_df.loc[index, "answer"]

    return "Sorry, I couldn't find an answer to that question."
