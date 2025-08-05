from state import State
from typing import Dict, Tuple
from utils.check_availability import AvailabilityService

def check_availability_node(state: State) -> State:
    """
    Checks if rooms are available for a given date and (optionally) room type and room count.
    Returns:
        - Next step ("ask_date", "ask_room_type", "ask_room_count", "no_availability", "proceed_to_price")
        - Updated state
    """
    Check = AvailabilityService()
    date = state.get("date")
    room_type = state.get("room_type")
    room_count = state.get("room_count")

    available, availability_data = Check.check_availability([date], room_type=room_type, room_count=room_count)


    state["availability_data"] = availability_data

    if not available:
        state["agent_message"] = availability_data
        return "wait_input", state

    if room_type and room_count:
        return "proceed_to_price", state
    elif not room_type and not room_count:
        return "ask_both", state
    elif not room_type:
        return "ask_room_type", state
    elif not room_count:
        return "ask_room_count", state
