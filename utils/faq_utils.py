import pandas as pd
from difflib import get_close_matches
import os
def load_faq_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # utils/
    path = os.path.join(base_dir, '..', 'knowledge_base', 'Hotel_faqs.csv')
    df = pd.read_csv(path)
    return df
def get_faq_answer(user_question, faq_df):
    questions = faq_df["question"].tolist()
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.5754)
    if matches:
        matched_question = matches[0]
        answer_row = faq_df[faq_df["question"] == matched_question]
        return answer_row["answer"].values[0]
    else:
        return "Sorry, I couldn't find an answer to that question."