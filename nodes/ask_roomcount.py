from state import State

def ask_room_count_node(state: State) -> State:
    room_type = state.get("room_type")
    available_data = state.get("availability_data", [])
    count = next((entry["available_rooms"] for entry in available_data if entry["room_type"] == room_type), 0)
    state["agent_message"] = f"{count} {room_type} rooms are available. How many would you like to book?"
    return state
