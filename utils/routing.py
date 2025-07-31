from utils.classify_intent import classify_intent_node
from state import State

def route_from_input(state: State) -> str:
    state = classify_intent_node(state)
    intent = state["intent"]
    if intent == "booking":
        print("➡️ Routing to node based on intent:", state["intent"])
        return "booking_node"
    elif intent == "faq":
        print("➡️ Routing to node based on intent:", state["intent"])
        return "faq_node"
    elif intent == "price_enquiry":
        print("➡️ Routing to node based on intent:", state["intent"])
        return "price_node"
    else:
        print("➡️ Routing to node based on intent:", state["intent"])   
        return "fallback_node"