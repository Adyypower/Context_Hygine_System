from typing import TypedDict, Annotated, List, Optional, Literal
from langchain_core.messages import BaseMessage
from app.core.models import HygieneMetrics

class AgentState(TypedDict):
    """
    Represents the state of the Context Governance Agent.
    """
    raw_messages: List[str]  # The raw input conversation
    current_query: str       # The user's new query
    
    # Hygiene Core Outputs
    optimized_context: Optional[str]
    hygiene_metrics: Optional[HygieneMetrics]
    drift_detected: bool
    hitl_required: bool
    
    # Advanced Governance Metadata
    query_intent: Optional[Literal["follow_up", "clarification", "topic_shift", "task_modification", "unrelated"]]
    degradation_level: Optional[Literal["none", "mild", "moderate", "severe"]]
    requires_reasoning_caution: Optional[bool]
    
    # Computed Manually (Not from LLM)
    context_version_id: Optional[str]

    # Final Output
    final_response: Optional[str]
