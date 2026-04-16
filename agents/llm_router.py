from enum import Enum
from dataclasses import dataclass
import os

class ModelTier(Enum):
    REASONING = "reasoning"      # complex decisions, negotiation, synthesis
    WORKHORSE = "workhorse"      # extraction, formatting, structured output
    BULK = "bulk"                # classification, tagging, sentiment at scale

@dataclass
class ModelConfig:
    provider: str
    model: str
    input_cost_per_m: float   # per million tokens
    output_cost_per_m: float
    max_context: int

# Updated Registry to use OpenAI only (since Anthropic key is missing)
MODEL_REGISTRY = {
    ModelTier.REASONING: ModelConfig(
        provider="openai",
        model="gpt-4o",
        input_cost_per_m=5.0,
        output_cost_per_m=15.0,
        max_context=128_000,
    ),
    ModelTier.WORKHORSE: ModelConfig(
        provider="openai",
        model="gpt-4o-mini",
        input_cost_per_m=0.15,
        output_cost_per_m=0.60,
        max_context=128_000,
    ),
    ModelTier.BULK: ModelConfig(
        provider="openai",
        model="gpt-4o-mini",
        input_cost_per_m=0.15,
        output_cost_per_m=0.60,
        max_context=128_000,
    ),
}

# Task-to-tier mapping
TASK_ROUTING = {
    # REASONING tier
    "sourcing.negotiation.compose_message": ModelTier.REASONING,
    "sourcing.negotiation.evaluate_response": ModelTier.REASONING,
    "sourcing.research.synthesize_report": ModelTier.REASONING,
    "marketing.budget.reallocation_plan": ModelTier.REASONING,
    "marketing.campaign.strategy_generation": ModelTier.REASONING,
    
    # WORKHORSE tier
    "supervisor.route_decision": ModelTier.WORKHORSE,
    "sourcing.research.score_product": ModelTier.WORKHORSE,
    "sourcing.supplier.rank_suppliers": ModelTier.WORKHORSE,
    "sourcing.qc.generate_checklist": ModelTier.WORKHORSE,
    "marketing.audience.build_segments": ModelTier.WORKHORSE,
    
    # BULK tier
    "sourcing.research.parse_listing": ModelTier.BULK,
    "sourcing.research.extract_reviews": ModelTier.BULK,
    "sourcing.supplier.parse_contact": ModelTier.BULK,
    "sourcing.research.classify_sentiment": ModelTier.BULK,
    "marketing.creative.tag_performance": ModelTier.BULK,
}

def get_model_for_task(task_type: str) -> ModelConfig:
    """
    Returns the model config for a given task.
    If WEAVE_DEV_MODE=true, overrides all tasks to use the BULK tier (cheapest).
    """
    is_dev_mode = os.getenv("WEAVE_DEV_MODE", "false").lower() == "true"
    
    if is_dev_mode:
        return MODEL_REGISTRY[ModelTier.BULK]
        
    tier = TASK_ROUTING.get(task_type, ModelTier.WORKHORSE)
    return MODEL_REGISTRY[tier]