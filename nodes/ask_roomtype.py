from state import State

def ask_room_type_node(state: State)->State:
    print("What type of room would you like to book? we have single,King,suite,luxury ")
    return state