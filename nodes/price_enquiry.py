from state import State
from utils.price_utils import  get_price_for_room
from llm import extract_booking_info

def price_enquiry_node(state: State) -> State:
    print("➡️ Routing to node based on intent: price_enquiry")
    user_input = state.get("user_input", "")
    extracted = extract_booking_info(user_input)

    room_type = extracted.get("room_type")
    if not room_type:
        return {**state, "response": "Could you please specify the room type?"}

    try:
          # This gives Dict[str, int]
        price = get_price_for_room(room_type)

        if price is not None:
            response = f"{room_type.title()} room costs ₹{price} per night."
        else:
            response = f"Sorry, we don't have a room type '{room_type}'."
        return {**state, "response": response}

    except Exception as e:
        print(f"[ERROR] price_enquiry_node: {e}")
        return {**state, "response": "Sorry, something went wrong while checking the price."}
