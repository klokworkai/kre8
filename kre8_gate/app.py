from fastapi import FastAPI
from pydantic import BaseModel

from kre8_agent.agent import call_llm
from kre8_think.engine import load_config, validate_plan
from kre8_think.models import Plan

app = FastAPI()

class IntentRequest(BaseModel):
    intent: str

@app.post("/plan")
def create_plan(request: IntentRequest):
    config = load_config()
    raw_plan = call_llm(request.intent)
    plan = Plan(**raw_plan)
    validate_plan(plan, config)
    return plan.dict()
