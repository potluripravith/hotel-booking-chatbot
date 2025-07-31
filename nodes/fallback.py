from utils.fallback_utils import generate_ai_fallback  

def fallback_node(state: dict) -> dict:
    user_input = state.get("user_input", "")
    ai_reply = generate_ai_fallback(user_input)
    print(f"🤖: {ai_reply}")
    return state
