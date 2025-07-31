from langgraph.graph import StateGraph,END
from state import State
from nodes.greet import greet_node
from nodes.wait_input import wait_input_node
from nodes.price_enquiry import price_enquiry_node  
from nodes.faq import faq_node                      
from nodes.booking import booking_node              
from nodes.fallback import fallback_node           
from utils.routing import route_from_input

def build_graph():
    workflow = StateGraph(State)
    
    workflow.add_node("greet", greet_node)
    workflow.add_node("wait_input",wait_input_node)
    workflow.add_node("booking_node", booking_node)
    workflow.add_node("faq_node", faq_node)
    workflow.add_node("price_node", price_enquiry_node)
    workflow.add_node("fallback_node", fallback_node)
    
    workflow.set_entry_point("greet")
    workflow.add_edge("greet","wait_input")
    workflow.add_conditional_edges("wait_input", route_from_input)
    for node in ["booking_node", "faq_node", "price_node", "fallback_node"]:
        workflow.add_edge(node, "wait_input")
    
    return workflow.compile()