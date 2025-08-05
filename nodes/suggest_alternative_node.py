from typing import Dict, Any
from state import State
from utils.suggest_alternative import RoomAvailabilityService


class AlternativeSuggestionService:
    def __init__(self, availability_service: RoomAvailabilityService):
        self.availability_service = availability_service

    def suggest(self, state: State) -> Dict[str, Any]:
        date = state.get("date")
        room_type = state.get("room_type")
        price = state.get("price")

        alternatives = self.availability_service.get_available_alternatives(date, exclude_room_type=room_type)
        cheaper = self.availability_service.suggest_cheaper_rooms(date, current_price=price) if price else []

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
