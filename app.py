from graph import build_graph

if __name__ == "__main__":
    app = build_graph()

    # Initial empty state
    state = {
        "user_input": None,
        "intent": None,
        "date": None,
        "room_type": None,
        "room_count": None,
        "available_rooms": None,
        "price": None,
    }

    # Step 1: Trigger initial greeting
    state = app.invoke(state)
    print("🤖:", state.get("response", "Welcome!"))

    # Step 2: Now loop for user interaction
    while True:
        user_input = input("👤: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖: Thank you! Have a great day!")
            break

        state["user_input"] = user_input
        state = app.invoke(state)

        print("🤖:", state.get("response", "I'm not sure how to help with that."))
