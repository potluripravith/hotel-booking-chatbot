from utils.fallback_utils import generate_ai_fallback  
from state import State
def fallback_node(state: State) -> State:
    user_input = state.get("user_input", "")
    ai_reply = generate_ai_fallback(user_input)
    state["agent_message"] = ai_reply  # Set agent message instead of printing
    return state
