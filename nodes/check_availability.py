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

    available, data = Check.check_availability(date, room_type=room_type, room_count=room_count)
    if available:
        if room_type and room_count is not None:
            state["agent_message"] = "Rooms are available. Proceeding to price calculation."
            return state
        else:
            state["agent_message"] = f"{data}"
            return state
        
    else:
        state["agent_message"] = f"{data}"
        return state