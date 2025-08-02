from llm import call_deepseek

def handle_confirmation_with_llm(state: dict) -> str:
    user_input = state.get("user_input", "")

    prompt = (
        f"The user was asked to confirm a hotel booking. Their response was: '{user_input}'.\n"
        "Does this indicate that they confirm the booking? Respond with only 'yes' or 'no'."
    )

    response = call_deepseek(prompt).strip().lower()
    
    if response == "yes":
        return "booking_confirmed"
    elif response == "no":
        return "suggest_alternative_node"
    else:
        return "fallback_node"
