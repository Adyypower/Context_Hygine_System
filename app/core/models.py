from pydantic import BaseModel, Field
from typing import Literal, Optional

class HygieneMetrics(BaseModel):
    relevance_retention_score: float = Field(..., description="Score between 0 and 1 indicating how much relevant information was retained.")
    context_reduction_ratio: float = Field(..., description="Ratio of tokens_after / tokens_before.")
    semantic_coherence_score: float = Field(..., description="Score between 0 and 1 indicating the semantic consistency of the optimized context.")

class HygieneOutput(BaseModel):
    # Core Fields (Required)
    optimized_context: str = Field(..., description="The cleaned and optimized context string.")
    tokens_before: int = Field(..., description="Estimated token count before processing.")
    tokens_after: int = Field(..., description="Estimated token count after processing.")
    compression_level: Literal["none", "light", "moderate", "aggressive"] = Field(..., description="The level of compression applied.")
    drift_detected: bool = Field(..., description="Whether semantic drift was detected between the new query and the context.")
    protected_items_count: int = Field(..., description="Number of critical information items protected from pruning.")
    hitl_required: bool = Field(..., description="Whether human intervention is required due to low confidence or ambiguity.")
    confidence: float = Field(..., description="Confidence score of the optimization process (0.0 to 1.0).")
    
    # Advanced Governance Fields (Optional/Heuristic)
    context_change_magnitude: Optional[float] = Field(None, description="Score (0-1) indicating magnitude of change from raw to optimized context.")
    degradation_level: Optional[Literal["none", "mild", "moderate", "severe"]] = Field(None, description="Assessment of context semantic loss.")
    query_intent: Optional[Literal["follow_up", "clarification", "topic_shift", "task_modification", "unrelated"]] = Field(None, description="Classification of the user's new query intent.")
    fragmentation_score: Optional[float] = Field(None, description="Score (0-1) indicating how fragmented/broken the logic chains are (0=cohesive).")
    requires_reasoning_caution: Optional[bool] = Field(None, description="Flag indicating if the downstream reasoner should proceed with caution.")

    metrics: HygieneMetrics
