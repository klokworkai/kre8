from pydantic import BaseModel

class Plan(BaseModel):
    workload_type: str
    region: str
    node_type: str
    node_count: int
    estimated_monthly_cost: float
