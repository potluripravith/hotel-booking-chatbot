from state import State
from llm import call_deepseek
from utils.price_utils import load_room_data, extract_room_prices, get_price_for_room

# nodes/price_enquiry.py
from state import State
from utils.price_utils import load_room_data, extract_room_prices, get_price_for_room

def price_enquiry_node(state: State) -> State:
    user_input = state.get("user_input", "")
    room_data = load_room_data()
    price_map = extract_room_prices(room_data)

    # Try to detect room type from user input
    found_room_type = None
    for r_type in ["single", "king", "suite", "luxury"]:
        if r_type in user_input.lower():
            found_room_type = r_type
            break

    if found_room_type:
        price = get_price_for_room(price_map, found_room_type)
        if price is not None:
            state["response"] = f"The price for a {found_room_type} room is ₹{price} per night."
        else:
            state["response"] = f"Sorry, we don't have the room type you specifed in our hotel."
    else:
        state["response"] = "Please specify the room type you're interested in (e.g., single, king, suite, luxury)."

    return state
