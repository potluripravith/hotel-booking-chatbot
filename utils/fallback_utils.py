from typing import List
from llm import call_deepseek

def generate_ai_fallback(user_input : str)-> str:
    """Uses deepseel Ai to generate a polite fallback message."""
    prompt = (
         f"The user said something off-topic: '{user_input}'. "
        "Please respond politely and guide them back to booking hotel rooms, "
        "checking availability, or asking about prices.")
    
    return call_deepseek(prompt)