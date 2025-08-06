
from state import State

def thank_you_node(state: State) -> State:
    state["thank_you_message"] = "Thank you for choosing our hotel booking service. We look forward to welcoming you!" 
    print(f"{state["thank_you_message"]}")
    return state
    

