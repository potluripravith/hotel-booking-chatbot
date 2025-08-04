from typing import List
from llm import call_deepseek

def generate_ai_fallback(user_input: str) -> str:
    """
    Uses DeepSeek AI to generate a polite fallback message for off-topic or unclear hotel-related queries.
    """
    prompt = (
        f"The user said: '{user_input}'. "
        "If the question is related to hotel booking but you don't know the answer, respond briefly and politely, saying you are unsure. "
        "If the question is unrelated to hotel booking, reply in one polite sentence saying the topic is off-topic."
        "Do not guess, hallucinate, or suggest external websites."
    )
    return call_deepseek(prompt)