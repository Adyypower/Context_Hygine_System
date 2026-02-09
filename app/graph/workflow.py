from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import hygiene_node, reasoning_node, human_review_node

def route_after_hygiene(state: AgentState):
    """
    Determines the next step after hygiene processing.
    """
    if state["hitl_required"]:
        return "human_review"
    return "reasoning_engine"

def build_graph(checkpointer=None):
    """
    Constructs the LangGraph workflow for the Hybrid Context Governance Agent.
    
    Args:
        checkpointer: Optional persistence layer (e.g., MemorySaver) for standalone testing.
                      In production, the parent system usually manages persistence.
    """
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("context_hygiene", hygiene_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("reasoning_engine", reasoning_node)
    
    # Define Edges
    workflow.set_entry_point("context_hygiene")
    
    # Conditional Edge
    workflow.add_conditional_edges(
        "context_hygiene",
        route_after_hygiene,
        {
            "human_review": "human_review",
            "reasoning_engine": "reasoning_engine"
        }
    )
    
    # End points
    workflow.add_edge("human_review", END)
    workflow.add_edge("reasoning_engine", END)
    
    return workflow.compile(checkpointer=checkpointer)
