from utils.faq_utils import load_faq_data
from utils.faq_utils import get_faq_answer

faq_df = load_faq_data()

def faq_node(state: dict) -> dict:
    user_input = state.get("user_input", "")
    answer = get_faq_answer(user_input, faq_df)
    print(f"🤖: {answer}")
    return state
