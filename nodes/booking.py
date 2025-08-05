from state import State
from llm import extract_booking_info

def booking_node(state:State)->State:
    user_input = state.get("user_input", "")
    # extracted = extract_booking_info(user_input)
    # if extracted is None:
    #     print("[ERROR] extract_booking_info returned None")
    #     state["date"] = []
    #     state["room_type"] = None
    #     state["room_count"] = None
    #     return state
    # dates = extracted.get("dates")
    
    # if dates is None:
    #     state["date"] = []
    # elif isinstance(dates, list):
    #     state["date"] = dates
    # else:
    #     state["date"] = [dates]
    # print(f"{state["date"]}")
    # state["room_type"] = extracted.get("room_type")
    # state["room_count"] = extracted.get("room_count")
    state["date"] = ['2025-08-01']
    print(state["date"])
    return state


