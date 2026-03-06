import os
import yaml

from .models import Plan
from .intent import extract_intent


def load_config():
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def validate_plan(plan: Plan, config: dict):
    if plan.workload_type not in config["workloads"]["allowed"]:
        raise ValueError("Workload not allowed")

    if plan.estimated_monthly_cost > config["constraints"]["max_budget_usd"]:
        raise ValueError("Budget exceeded")

    return True


def process_intent(raw_input: str, agent):
    """
    Main I2D2 orchestration entry point.

    Flow:
        raw input
        ↓
        intent extraction
        ↓
        (future) design reasoning
        ↓
        plan validation
    """

    # Step 1 — extract structured intent
    # (for now we reuse the existing stub agent call)
    intent = extract_intent(raw_input, agent)

    # Step 2 — placeholder design logic
    # (for now we reuse the existing stub agent call)
    plan_data = agent.call_llm(intent.goal)

    plan = Plan(**plan_data)

    # Step 3 — validate against platform config
    config = load_config()
    validate_plan(plan, config)

    return plan