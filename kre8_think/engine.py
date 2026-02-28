import os
import yaml
from .models import Plan

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
