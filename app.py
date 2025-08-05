from graph import build_graph
from state import State



if __name__ == "__main__":
    app = build_graph()
    state: State = {
        "user_input": None,
        "intent": None,
        "has_greeted": False,
        "date": None,
        "room_type": None,
        "room_count": None,
        "price": None,
        "total_price": None,
        "fallback_message": None,
        "agent_message": None,
        "thank_you_message": None,
        "availability_data": None,
        "memory": []  # Required for tracking conversation context
    }
    state: State = app.invoke(state)
    print("🤖:", state.get("response", "Welcome!"), flush=True)

    while True:
        user_input = input("👤: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖: Thank you! Have a great day!")
            break
        state["user_input"] = user_input
        state = app.invoke(state)

