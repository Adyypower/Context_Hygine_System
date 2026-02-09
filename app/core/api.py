from typing import List, Dict, Any, Optional
from app.core.hygiene import ContextHygieneController

def sanitize_context(
    history: List[str], 
    query: str, 
    llm: Optional[Any] = None,
    prompt_type: str = "optimized"
) -> Dict[str, Any]:
    """
    Middleware Function: Intercepts and sanitizes context before reasoning.

    Args:
        history: List of previous conversation strings.
        query: The new user query.
        llm: Optional custom LLM instance (LangChain).
        prompt_type: "optimized" (default), "standard", or "opensource".

    Returns:
        Dict containing:
        - 'status': 'pass' or 'halt'
        - 'content': Optimized context string (if pass) or Rejection message (if halt)
        - 'metadata': Full hygiene metrics
    """
    # 1. Initialize Controller
    governor = ContextHygieneController(llm=llm, prompt_type=prompt_type)

    # 2. Run Optimization
    result = governor.optimize_context(
        raw_context=history,
        new_query=query
    )

    # 3. Apply Decision Logic (The "Firewall")
    if result.hitl_required:
        return {
            "status": "halt",
            "reason": "Governance Violation: Human Review Required",
            "content": f"[SYSTEM]: I detected a risky topic shift (Intent: {result.query_intent}). Please clarify before proceeding.",
            "metadata": result.model_dump()
        }
    
    # 4. Success Case
    return {
        "status": "pass",
        "content": result.optimized_context,
        "metadata": result.model_dump()
    }
