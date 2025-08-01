
from state import State

def agent_node(state: State) -> State:
    return {
        **state,
        "agent_message": "Our hotel agent will contact you shortly with the booking confirmation and further details."
    }

