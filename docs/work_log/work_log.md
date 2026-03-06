# kre8 – Work Log

Chronological record of **coding work and repo-related activities** for the `kre8-framework-demo` repository.

---

## 2026-03-05

### Objective
Start the first tangible implementation for the **NLP intent extraction pipeline** and wire it into the existing FastAPI demo flow.

### Repo / Coding Work Completed
- Added `kre8_think/intent_models.py`
- Defined initial `StructuredIntent` schema
- Added `kre8_think/intent.py`
- Implemented `extract_intent(raw_input, agent)` as the intent extraction entry point
- Refactored `kre8_agent/agent.py` into a class-based stub:
  - `Kre8Agent.call_llm()`
  - `Kre8Agent.extract_intent()`
- Renamed `kre8_think/engine.py` to `kre8_think/i2d2.py`
- Updated I2D2 orchestration flow to:
  - extract intent
  - call stub design generation
  - validate plan
- Updated `kre8_gate/app.py` imports and flow to use:
  - `Kre8Agent`
  - `process_intent()`

### Architecture Decisions Applied in Code
- Dropped the earlier hybrid heuristic parsing approach
- Adopted **LLM-only intent extraction flow**
- Kept `extract_intent()` as the stable interface
- Kept agent interactions isolated in `kre8_agent`
- Kept current design generation and intent extraction as **stubs** for now

### Validation / Testing Completed
- Created local virtual environment workflow
- Confirmed dependency setup approach using `.venv`
- Started FastAPI app successfully with Uvicorn
- Executed successful curl test against:

```bash
POST /plan
```

### Observed Result
The API returned the expected stubbed plan JSON:

```json
{
  "workload_type": "eks-dev",
  "region": "us-east-1",
  "node_type": "t3.small",
  "node_count": 1,
  "estimated_monthly_cost": 72.0
}
```

### Notes
- End-to-end flow is now working through the new architecture
- Output is still stubbed, which is expected at this stage

### Next Coding Step
- Surface `StructuredIntent` more explicitly for debugging / visibility
- Begin replacing stub behavior incrementally
- Move from curl-based interaction toward a simple UI-based interaction layer
