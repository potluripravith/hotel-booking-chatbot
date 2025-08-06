from utils.price_utils import PriceCalculator
from state import State

def price_calculation_node(state:State)->State:

    """
    Calculates total booking price for given room type, count, and dates.
    
    """
    room_type=state.get("room_type")
    room_count = state.get("room_count")
    dates = state.get("dates",[])
    price = PriceCalculator()
    if not room_type or not room_count or not dates:
        state["agent_message"] = "Booking details are incomplete. Please provide room type, room count, and valid dates."
        return state
    nights = len(dates)
    

    total_price = price.calculate_total_price(room_type, nights, room_count)

    if total_price == 0:
        state['agent_message'] = f"Sorry, we couldn't calculate the price for the '{room_type}' room."
        return state
    state["total_price"] = total_price
    state["agent_message"] = f"Yes, the {room_type} room is available for {room_count} rooms over {nights} nights. The total price is ₹{total_price}. Shall I proceed to book?"

    return state

