from state import State
from utils.conversation_utils import add_to_conversation
def print_response(state: State) -> State:
    
    if state.get("agent_message"):
        print(f"🤖: {state['agent_message']}")
          
    user_input = state.get("user_input")
    agent_msg = state.get("agent_message")
    add_to_conversation(state, user_input,agent_msg)
    state["agent_message"] = None
    state["user_input"] = None
    
    
    return state