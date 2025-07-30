from state import State

def wait_input_node(state:State)->State:
    user_message = input("👤:")
    state["user_input"] = user_message
    return state