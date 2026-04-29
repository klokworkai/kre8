import konnekt as konnekt_module
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from konnekt.errors import KonnektError
from .i2d2 import process_intent

app = FastAPI(title="i2d2", version="0.1.0", description="kre8 reasoning engine")


class IntentRequest(BaseModel):
    input: str


@app.get("/health")
def health():
    return {"status": "ok", "component": "i2d2"}


@app.post("/process")
def process(request: IntentRequest):
    try:
        kit = process_intent(request.input, konnekt=konnekt_module)
        return kit.model_dump()
    except KonnektError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
