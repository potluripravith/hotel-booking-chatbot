from state import State
from llm import extract_booking_info

def booking_node(state:State)->State:
    user_input = state.get("user_input", "")
    extracted = extract_booking_info(user_input)
    dates = extracted.get("dates")

    state["date"] = dates
    state["room_type"] = extracted.get("room_type")
    state["room_count"] = extracted.get("room_count")

    return state


