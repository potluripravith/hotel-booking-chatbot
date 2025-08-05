from state import State
from utils.price_utils import PriceCalculator
from llm import extract_booking_info

def price_enquiry_node(state: State) -> State:
    # print("➡️ Routing to node based on intent: price_enquiry")
    price = PriceCalculator()
    # user_input = state.get("user_input", "")
    # extracted = extract_booking_info(user_input)
    

    # room_type = extracted.get("room_type")
    room_type = "single"
    print(f"room_type: {room_type}")
    if not room_type:
        return {**state, "response": "Could you please specify the room type?"}


        # This gives Dict[str, int]
    price = price.get_price_for_room(room_type)
    print(f"price:{price}")

    if price is not None:
        state["agent_message"] = f"{room_type.title()} room costs ₹{price} per night."
        # print(f"{response}")
    else:
        state["agent_message"] = f"Sorry, we don't have a room type '{room_type}'."
    return state
