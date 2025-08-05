from utils.faq_utils import FAQAnswerService
from state import State
faq_service = FAQAnswerService()

def faq_node(state: State) -> State:
    user_input = state.get("user_input", "")
    response = faq_service.get_answer(user_input)
    state["agent_message"] = response
    return state
