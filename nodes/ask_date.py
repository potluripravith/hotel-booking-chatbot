from state import State

def ask_date_node(state:State) -> State:
    state["agent_message"] = "Could you please provide your check-in date?"
    return state

