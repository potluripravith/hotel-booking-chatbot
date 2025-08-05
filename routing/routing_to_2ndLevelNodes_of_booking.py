from state import State

def route_booking_info_node(state: State) -> str:
    if not state.get("date"):
        return "ask_date"
    else:
        return "check_availability"