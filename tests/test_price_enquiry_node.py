# test_price_node.py
from nodes.price_enquiry import price_enquiry_node

state = {
    "user_input": "what is the price of single room?",
    "intent": "price_enquiry"
}

result = price_enquiry_node(state)
print("💬 Bot response:", result.get("response"))
