from utils.classify_intent import classify_intent_node
from state import State

def route_from_input(state: State) -> str:
    state = classify_intent_node(state)
    intent = state["intent"]
    if intent == "booking":
        return "booking_node"
    elif intent == "faq":
        return "faq_node"
    elif intent == "price_enquiry":
        return "price_node"
    else:
        return "fallback_node"