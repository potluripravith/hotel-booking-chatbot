from state import State
def ask_room_type_and_count_node(state: State) -> State:
    available_data = state.get("availability_data", [])
    summary = "\n".join([f"{entry['room_type']}: {entry['available_rooms']} rooms" for entry in available_data])
    state["agent_message"] = f"Here are the available options:\n{summary}\nPlease provide the room type and number of rooms you'd like to book."
    return state

