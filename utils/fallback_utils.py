from typing import List
from llm import call_deepseek

def is_irrelevant_input(user_input : str, valid_keywords: List[str]) -> bool:
    """determines whether the user's input is irrelvant to the known keywords"""
    user_input = user_input.lower()
    return not any( keyword in user_input for keyword in valid_keywords)

def generate_ai_fallback(user_input : str)-> str:
    """Uses deepseel Ai to generate a polite fallback message."""
    prompt = (
         f"The user said something off-topic: '{user_input}'. "
        "Please respond politely and guide them back to booking hotel rooms, "
        "checking availability, or asking about prices.")
    
    return call_deepseek(prompt)