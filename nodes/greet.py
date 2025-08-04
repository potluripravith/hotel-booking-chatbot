from state import State

def greet_node(state: State) -> State:
    if state.get("has_greeted"):
        return state  # Skip greeting if already done

    print("🤖: Hello! Welcome to our hotel booking assistant.")
    print("🤖: How can I assist you today?")
    state["has_greeted"] = True
    return state

