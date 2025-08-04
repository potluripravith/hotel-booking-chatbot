from state import State
def print_response(state: State) -> State:
    if state.get("agent_message"):
        print(f"🤖: {state['agent_message']}")
        state["response"] = None  
    return state