from state import State

def booking_confirmed_node(state: State) -> State:
    # print("✅ Your booking has been confirmed!")
    state["booking_status"] = "confirmed"
    return state
