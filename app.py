from graph import build_graph
from state import State



if __name__ == "__main__":
    app = build_graph()
    state: State = app.invoke({})
    print("🤖:", state.get("response", "Welcome!"), flush=True)

    while True:
        user_input = input("👤: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🤖: Thank you! Have a great day!")
            break
        state["user_input"] = user_input
        state = app.invoke(state)

