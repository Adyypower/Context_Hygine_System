import hashlib
from app.graph.state import AgentState
from app.core.hygiene import ContextHygieneController

# Initialize controller once (or per node execution if needed)
hygiene_controller = ContextHygieneController()

def compute_version_id(text: str) -> str:
    """Computes a deterministic hash for the context version."""
    if not text:
        return "v0"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

def hygiene_node(state: AgentState) -> AgentState:
    """
    Executes the Context Hygiene Controller to optimize the raw context.
    """
    print("--- Hygiene Node: Optimizing Context ---")
    raw = state["raw_messages"]
    query = state["current_query"]
    
    # Call the tool
    result = hygiene_controller.optimize_context(
        raw_context=raw,
        new_query=query,
        max_token_threshold=2000 # Configurable
    )
    
    # Compute deterministic version ID
    version_id = compute_version_id(result.optimized_context)

    # Update State with ALL governance metadata
    return {
        "optimized_context": result.optimized_context,
        "hygiene_metrics": result.metrics,
        "drift_detected": result.drift_detected,
        "hitl_required": result.hitl_required,
        # Advanced Metadata
        "query_intent": result.query_intent,
        "degradation_level": result.degradation_level,
        "context_version_id": version_id,
        "requires_reasoning_caution": result.requires_reasoning_caution
    }

def human_review_node(state: AgentState) -> AgentState:
    """
    Triggered when hygiene confidence is low or drift is detected.
    Instead of crashing, it asks the user for clarification.
    """
    print("--- HUMAN REVIEW NODE Triggered ---")
    intent = state.get("query_intent", "unknown")
    drift = state.get("drift_detected", False)
    
    if drift:
        response = (
            f"I noticed a significant topic shift (Intent: {intent}). "
            "To avoid confusion, would you like me to clear the previous context and start fresh?"
        )
    else:
        response = (
            "I'm not fully confident in how to merge this new request with our previous conversation. "
            "Could you clarify if this is a follow-up or a new task?"
        )
    
    return {"final_response": f"[SYSTEM GOVERNANCE]: {response}"}

def reasoning_node(state: AgentState) -> AgentState:
    """
    Placeholder for the main Gemini reasoning step.
    Uses the *optimized* context, not the raw one.
    """
    print("--- Reasoning Node: Generating Response ---")
    
    # Check for caution flag
    if state.get("requires_reasoning_caution"):
        print("WARNING: Reasoning Caution Flag is active! Entropy or Degradation is high.")
    
    context = state["optimized_context"]
    query = state["current_query"]
    
    # In a real impl, this would call Gemini.generate_content(context + query)
    response = f"[MOCK RESPONSE based on optimized context]: {context[:50]}..."
    
    return {"final_response": response}
