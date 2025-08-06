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
from nodes.ask_room_type_and_count import ask_room_type_and_count_node
from nodes.check_availability import check_availability_node
from nodes.booking_confirmed import booking_confirmed_node
from nodes.price_calculation import price_calculation_node
# from nodes.suggest_alternative_node import AlternativeSuggestionService
from nodes.thank_you import thank_you_node
from nodes.agent_node import agent_node           
from routing.routing_to_1st_level_nodes import route_from_input
from nodes.print_response import print_response
from routing.routing_to_2ndLevelNodes_of_booking import route_booking_info_node
        
def build_graph():
    workflow = StateGraph(State)
    
    workflow.add_node("greet", greet_node)
    workflow.add_node("wait_input",wait_input_node)
    workflow.add_node("booking_node", booking_node)
    workflow.add_node("faq_node", faq_node)
    workflow.add_node("print_response", print_response)
    workflow.add_node("price_node", price_enquiry_node)
    workflow.add_node("fallback_node", fallback_node)
    workflow.add_node("ask_date",ask_date_node)
    workflow.add_node("ask_room_type", ask_room_type_node)
    workflow.add_node("ask_room_count", ask_room_count_node)
    workflow.add_node("ask_room_type_and_count", ask_room_type_and_count_node)
    workflow.add_node("check_availability", check_availability_node)
    # workflow.add_node("suggest_alternative_node", suggest_alternative_node)
    workflow.add_node("price_calculation", price_calculation_node)
    workflow.add_node("confirming_booking_node", booking_confirmed_node)

    workflow.add_node("agent_node", agent_node)
    workflow.add_node("thank_you_node", thank_you_node)
    
    
    
    workflow.set_entry_point("greet")
    workflow.add_edge("greet","wait_input")
    workflow.add_conditional_edges(
    "wait_input",
    route_from_input,
    {
        "booking_node": "booking_node",
        "faq_node": "faq_node",
        "price_node": "price_node",
        "confirming_booking_node":"confirming_booking_node",
        # "suggest_alternative_node":"suggest_alternative_node",
        "thank_you_node":"thank_you_node",
        "fallback_node": "fallback_node"
    }
)
    workflow.add_conditional_edges("booking_node", route_booking_info_node, {
        "ask_date": "ask_date",
        "check_availability": "check_availability"
    })
    
    workflow.add_conditional_edges(
    "check_availability",
    lambda state: state.next,  
    {
        "ask_room_type": "ask_room_type",
        "ask_room_count": "ask_room_count",
        "ask_room_type_and_count": "ask_room_type_and_count",
        "proceed_to_price": "price_calculation"
    }
)



    workflow.add_edge("confirming_booking_node", "agent_node")
    workflow.add_edge("price_node", "print_response")
    workflow.add_edge("faq_node", "print_response")
    workflow.add_edge("fallback_node", "print_response")
    workflow.add_edge("ask_date", "print_response")
    workflow.add_edge("check_availability", "print_response")
    workflow.add_edge("ask_room_type", "print_response")
    workflow.add_edge("ask_room_count", "print_response")
    workflow.add_edge("ask_room_type_and_count", "print_response")
    workflow.add_edge("price_calculation", "print_response")
    workflow.add_edge("agent_node","print_response")
    workflow.add_edge("print_response", "wait_input")
    


    workflow.set_finish_point("thank_you_node")
    


    return workflow.compile()



# def save_graph_as_png():
#     workflow = build_graph()
#     graph = workflow.get_graph()
#     png_data = graph.draw_mermaid_png()
#     with open("fixed_hotel_booking_graph.png", "wb") as f:
#         f.write(png_data)

#     print("Graph saved as hotel_booking_graph.png")

# if __name__ == "__main__":
#     save_graph_as_png()