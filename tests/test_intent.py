from utils.classify_intent import classify_intent_node

def test_intent_classification(user_input: str):
    state = {"user_input": user_input, "intent": None}
    updated_state = classify_intent_node(state)
    print(f"User Input: {user_input}")
    print(f"Classified Intent: {updated_state['intent']}")
    print("-" * 50)

# Test samples
test_intent_classification("I want to room from Aug 3rd to Aug 5th")
test_intent_classification("What time is check-in?")
test_intent_classification("How much does a single room cost?")
test_intent_classification("Tell me a joke")
