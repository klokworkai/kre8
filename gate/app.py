from fastapi import FastAPI
from pydantic import BaseModel

from kre8_agent.agent import Kre8Agent
from kre8_think.i2d2 import process_intent

app = FastAPI()

agent = Kre8Agent()


class IntentRequest(BaseModel):
    intent: str


@app.post("/plan")
def create_plan(request: IntentRequest):
    plan = process_intent(request.intent, agent)
    return plan.model_dump()