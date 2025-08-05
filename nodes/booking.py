from state import State
from llm import extract_booking_info

def booking_node(state:State)->State:
    user_input = state.get("user_input", "")
    # extracted = extract_booking_info(user_input)
    date = None
    state["date"] = date
    # if extracted.get("date"):
    #     state["date"] = extracted["date"]
    # if extracted.get("room_type"):
    #     state["room_type"] = extracted["room_type"]
    # if extracted.get("room_count"):
    #     state["room_count"] = extracted["room_count"]

    return state