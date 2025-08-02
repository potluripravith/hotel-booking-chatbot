from state import State
from typing import Dict, Tuple
from utils.booking_utils import check_availability

def check_availability_node(state: Dict) -> Tuple[str, Dict]:
    """
    Checks if rooms are available for a given date and (optionally) room type and room count.
    Returns:
        - Next step ("ask_date", "ask_room_type", "ask_room_count", "no_availability", "proceed_to_price")
        - Updated state
    """
    date = state.get("date")
    room_type = state.get("room_type")
    room_count = state.get("room_count")

    # Step 1: Ask for missing date
    if not date:
        return "ask_date", state
    available, data = check_availability([date], room_type=room_type, room_count=room_count)
    if available:
        if room_type and room_count is not None:
            return "proceed_to_price",state
        else:
            return f"{data}"
        
    else:
        return f"{date}"