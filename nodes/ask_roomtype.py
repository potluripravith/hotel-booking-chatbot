from state import State

def ask_room_type_node(state: State)->State:
    available_data = state.get("availability_data", [])
    room_types = list({entry['room_type'] for entry in available_data})
    state["agent_message"] = f"Available room types: {', '.join(room_types)}. Which would you like to book?"
    return state