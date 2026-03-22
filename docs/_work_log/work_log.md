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


---

## 2026-03-21

### Objective
Refine the product architecture and repo/documentation structure before introducing the first UI slice.

### Architecture / Product Work Completed
- Simulated the intended end-user workflow from Kiosk through SI, validation, pause, and DP delivery.
- Refined the SI checkpoint behavior:
  - SI is always generated
  - validation occurs before plan generation
  - the user is paused at a **Go / Review** checkpoint
- Established that the request flow must be **realm-aware** because users assume existing defaults and platform context.
- Defined the role of `kre8_realm` as the scoped operating context.
- Confirmed that `kre8_laws` should remain reusable and globally defined, with realms binding to law sets rather than duplicating them.
- Finalized **ARC** as the Architecture Catalog for reuse, retention, and user selection.
- Named the admin/configuration surface **Whiteboard**.
- Reviewed the current repository structure and produced a recommended near-term tree that preserves top-level components and adds new top-level component folders instead of introducing a `components/` root.
- Produced missing README content for new and existing components and for hybrid central docs areas.

### Repo / Documentation Direction Applied
- Preserve existing top-level code component layout.
- Add these new top-level component folders:
  - `kre8_kiosk`
  - `kre8_whiteboard`
  - `kre8_realm`
  - `kre8_laws`
  - `kre8_arc`
- Keep hybrid documentation:
  - central `docs/` for product/system concepts
  - component-local READMEs for later lift-and-shift

### Notes
- No code execution path was changed today.
- Work was focused on architectural clarity, component naming, flow design, and documentation structure.

### Next Coding / Repo Step
- Normalize folders and canonical doc filenames in the repo.
- Re-upload the updated repo tree/zip.
- Generate and place the canonical README and central docs files into the aligned structure.
