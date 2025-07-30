from graph import build_graph
if __name__=="__main__":
    app = build_graph()
    initial_state = {
        "user_input": None,
        "intent": None,
        "date": None,
        "room_type": None,
        "room_count": None,
        "available_rooms": None,
        "price": None,
    }
    app.invoke(initial_state)
