from langgraph.graph import StateGraph,END
from state import State
from nodes.greet import greet_node
from nodes.wait_input import wait_input_node
from nodes.price_enquiry import price_enquiry_node  
from nodes.faq import faq_node                      
from nodes.booking import booking_node              
from nodes.fallback import fallback_node
from nodes.ask_date import ask_date_node
from nodes.ask_roomtype import ask_room_type_node
from nodes.ask_roomcount import ask_room_count_node
from nodes.check_availability import check_availability_node
from nodes.booking_confirmed import booking_confirmed_node
from nodes.confirmation_booking import confirmation_node
from nodes.price_calculation import price_calculation_node
from nodes.suggest_alternative_node import suggest_alternative_node
from nodes.thank_you import thank_you_node
from nodes.agent_node import agent_node           
from utils.routing import route_from_input
from handle_conformation import handle_confirmation_with_llm

def build_graph():
    workflow = StateGraph(State)
    
    workflow.add_node("greet", greet_node)
    workflow.add_node("wait_input",wait_input_node)
    workflow.add_node("booking_node", booking_node)
    workflow.add_node("faq_node", faq_node)
    workflow.add_node("price_node", price_enquiry_node)
    workflow.add_node("fallback_node", fallback_node)
    workflow.add_node("ask_date",ask_date_node)
    workflow.add_node("ask_room_type", ask_room_type_node)
    workflow.add_node("ask_room_count", ask_room_count_node)
    workflow.add_node("check_availability", check_availability_node)
    workflow.add_node("suggest_alternative", suggest_alternative_node)
    workflow.add_node("price_calculation", price_calculation_node)
    workflow.add_node("confirmation_booking", confirmation_node)
    workflow.add_node("booking_confirmed", booking_confirmed_node)
    workflow.add_node("agent_node", agent_node)
    workflow.add_node("thank_you", thank_you_node)
    
    
    
    workflow.set_entry_point("greet")
    workflow.add_edge("greet","wait_input")
    workflow.add_conditional_edges("wait_input", route_from_input)
    for node in ["booking_node", "faq_node", "price_node", "suggest_alternatie","fallback_node"]:
        workflow.add_edge(node, "wait_input")
    workflow.add_conditional_edges("booking_node", lambda state: "ask_date" if not state.get("date") else "check_availability", {
        "ask_date": "ask_date",
        "check_availability": "check_availability"
    })
    workflow.add_edge("ask_date", "check_availability")
    workflow.add_conditional_edges("check_availability", lambda state: (
        "ask_room_type" if not state.get("room_type") else 
        "ask_room_count" if not state.get("room_count") else 
        "price_calculation"
    ), {
        "ask_room_type": "ask_room_type",
        "ask_room_count": "ask_room_count",
        "price_calculation": "price_calculation"
    })

    # After asking missing data → recheck availability
    workflow.add_edge("ask_room_type", "check_availability")
    workflow.add_edge("ask_room_count", "check_availability")
    
    workflow.add_edge("price_calculation", "confirmation_booking")
    workflow.add_conditional_edges("confirmation_booking", handle_confirmation_with_llm)
    workflow.add_edge("booking_confirmed", "agent_node")
    workflow.add_edge("agent_node", "thank_you")
    


    workflow.set_finish_point("thank_you")




    return workflow.compile()