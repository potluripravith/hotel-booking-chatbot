from typing import List
from state import State
from llm import call_deepseek

INTENTS = ["booking", "faq", "price_enquiry", "proceed_booking", "alternative", "thank_you"]

def classify_intent_node(state: State) -> State:
    user_input = state.get("user_input", "")
    conversation_history: List[str] = state.get("memory", [])
    recent_history = "\n".join(conversation_history[-2:]) if conversation_history else ""
    print(f"{recent_history}")
    print(f"{conversation_history}")

    prompt = f"""Classify the following user input into one of the intents:
    - booking: if it's about booking a room.
    - faq: if it's a general question like check-in time, wifi availability, etc.
    - price_enquiry: if it's asking about the cost of rooms.
    - proceed_booking: if the user confirms or wants to proceed with the booking after a price is shown.
    - alternative: if the user says the price is too high or asks for a cheaper option.
    - thank_you: if the user ends the conversation politely or decides not to proceed.
    - fallback: if it doesn't fit any category clearly.

    **IMPORTANT**: Base your classification mainly on the current input. Use recent messages only if the current input is vague or requires context.

    Recent Conversation:
    {recent_history}

    Current User Input: "{user_input}" 

    Respond with only one word: booking, faq, price_enquiry, proceed_booking, alternative, thank_you, or fallback.
    """

    response = call_deepseek(prompt)
    intent = response.strip().lower()

    if intent not in INTENTS + ["fallback"]:
        intent = "fallback"


    state["intent"] = intent
    return state
