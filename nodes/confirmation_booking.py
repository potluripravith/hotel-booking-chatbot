from state import State

def confirmation_node(state: State) -> State:
    confirmation_message = (
        f"The total price will be ₹{state['total_price']}.\n"
        "Should I proceed with the booking?"
    )
    print(confirmation_message)
    return state