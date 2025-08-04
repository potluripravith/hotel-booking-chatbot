from state import State
from typing import Dict, Any
from utils.price_utils import load_room_data
from utils.suggest_alternative import get_available_alternatives,suggest_cheaper_rooms

def suggest_alternative_node(state: State) -> Dict[str, Any]:
    """
    Suggest alternative room types or cheaper options when the requested room is unavailable.
    """
    date = state.get("date")
    room_type = state.get("room_type")
    price = state.get("price")

    df = load_room_data()

    # Suggest other room types with availability
    alternatives = get_available_alternatives(df, date, exclude_room_type=room_type)

    # Suggest cheaper room types (optional if original room has a price)
    cheaper = []
    if price is not None:
        cheaper = suggest_cheaper_rooms(df, date, current_price=price)

    if not alternatives and not cheaper:
        return {
            "alternative_suggestion": "Unfortunately, there are no alternative rooms available for the selected date.",
            "alternative_rooms": [],
            "cheaper_options": []
        }

    messages = []
    if alternatives:
        alt_msg = "\n".join(
            f"- {r_type} ({count} rooms available at ₹{r_price})"
            for r_type, count, r_price in alternatives
        )
        messages.append("Here are some available alternatives:\n" + alt_msg)

    if cheaper:
        cheap_msg = "\n".join(
            f"- {r_type} at ₹{r_price}"
            for r_type, r_price in cheaper
        )
        messages.append("You may also consider these cheaper rooms:\n" + cheap_msg)

    return {
        "alternative_suggestion": "\n\n".join(messages),
        "alternative_rooms": alternatives,
        "cheaper_options": cheaper
    }
