from typing import Literal
from state import State
from llm import call_deepseek


INTENTS = ["booking", "faq", "price_enquiry"]

def classify_intent_node(state:State)->State:
    # user_input = state.get("user_input","")
    # # prompt = f"""Classify the following user input into one of the intents:
    # # - booking: if it's about booking a room.
    # # - faq: if it's a general question like check-in time, wifi etc.
    # # - price_enquiry: if it's about room prices.
    # # If it doesn't fit any, respond with "fallback".
    # # User input: \"{user_input}\"
    # # Respond with only one word: booking, faq, price_enquiry, or fallback."""
    # # response = call_deepseek(prompt)
    # # intent = response.strip().lower()
    
    # if intent not in INTENTS + ["fallback"]:
    #     intent = "fallback"
        
    state["intent"] = "price_enquiry"
    return state

