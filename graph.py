from langgraph.graph import StateGraph,END
from state import State
from nodes.greet import greet_node
from nodes.wait_input import wait_input_node

def build_graph():
    workflow = StateGraph(State)
    
    workflow.add_node("greet", greet_node)
    workflow.add_node("wait_input",wait_input_node)
    
    
    workflow.set_entry_point("greet")
    workflow.add_edge("greet","wait_input")
    workflow.add_edge("wait_input",END)
    
    return workflow.compile()