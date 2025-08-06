#conversation_utils.py

def add_to_conversation(state, user_message: str, agent_message: str):
    if user_message:
        state["memory"].append(f"user: {user_message}")
    if agent_message:
        state["memory"].append(f"agent: {agent_message}")