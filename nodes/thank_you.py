
from state import State

def thank_you_node(state: State) -> State:
    return {
        **state,
        "thank_you_message": "Thank you for choosing our hotel booking service. We look forward to welcoming you!"
    }

