# kre8 – System State Log

> Living architectural state and evolution record of the kre8 Thinking Platform Layer (TPL)

---

## Project Identity

**Name:** kre8  
**Type:** Thinking Platform Layer (TPL) framework  
**Current Version:** 0.01.0  
**Repository Mode:** Mono-repo demo (`kre8-framework-demo`)  
**Status:** Working skeleton with first intent extraction path wired end-to-end

---

# 🧭 Current Architecture Snapshot

## Components (current)

- **kre8_gate**  
  FastAPI ingress layer (HTTP entry point)

- **kre8_think**  
  Core TPL reasoning layer  
  - extracts intent
  - orchestrates I2D2 flow
  - loads config
  - validates generated plan

- **I2D2**  
  Internal engine inside `kre8_think`  
  - Intelligent Infrastructure Design Decision
  - orchestrates intent → plan flow

- **kre8_agent**  
  LLM adapter layer (currently stubbed)  
  - `extract_intent()` stub
  - `call_llm()` stub

- **kre8_cli**  
  Placeholder CLI client

---

# 🔐 Locked Architectural Decisions

- kre8 is a **Thinking Platform Layer**
- LLM returns structured JSON only
- No raw LLM-generated Terraform is executed
- Deterministic Terraform generation remains a later phase
- `kre8_laws` will follow the **LADE** model
- `I2D2` means **Intelligent Infrastructure Design Decision**
- Intent extraction approach has moved to **LLM-only**
- `extract_intent()` is the stable parser entry point
- Agent interactions remain isolated inside `kre8_agent`
- Mono-repo structure remains the correct shape for this phase

---

# 🧠 Conceptual Definition

kre8 is a Thinking Platform Layer above the control plane.

It separates:
- Intent extraction
- Reasoning
- Validation
- Rendering (future)
- Execution (future)

LLM is a suggestion / extraction engine, not authority.

---

# 🚧 Active Phase

### 0.01.0 – Thinking Mode (Lite)

Capabilities currently working:
- Accept intent via FastAPI
- Use `Kre8Agent.extract_intent()` stub
- Convert intent through `extract_intent()` into `StructuredIntent`
- Use `Kre8Agent.call_llm()` stub to generate a placeholder plan
- Validate plan via Pydantic
- Validate plan against YAML config
- Return structured JSON through the `/plan` endpoint

Not yet implemented:
- Real Bedrock integration
- Real intent extraction
- DesignPlan generation
- Terraform rendering
- Provisioning
- State store
- Async workers

---

# 🧩 Current File-Level Direction

## `kre8_think`
- `i2d2.py` → orchestration entry point
- `intent.py` → intent extraction wrapper
- `intent_models.py` → `StructuredIntent`
- `models.py` → `Plan`
- `config.yaml` → validation constraints

## `kre8_agent`
- `agent.py` → class-based stub agent

## `kre8_gate`
- `app.py` → FastAPI entry point calling `process_intent()`

---

# 📅 Daily Log

---

## 2026-03-05

### What Was Done
- Renamed `engine.py` to `i2d2.py`
- Added `StructuredIntent` model in `intent_models.py`
- Added `intent.py` with `extract_intent()`
- Refactored `agent.py` into class-based `Kre8Agent`
- Added stub methods:
  - `extract_intent()`
  - `call_llm()`
- Updated FastAPI gate imports and flow
- Created and used local `.venv`
- Ran Uvicorn successfully
- Performed successful curl test against `/plan`

### Decisions Made
- Dropped hybrid heuristic extraction
- Switched to **LLM-only intent extraction path**
- Kept both agent methods for future Bedrock integration
- `i2d2.py` remains the orchestration layer
- Current returned plan is allowed to remain stubbed

### Technical Discoveries
- VSCode interpreter issue was caused by environment selection, not broken code
- Current end-to-end path is functioning correctly
- Stub architecture is sufficient to validate the pipeline shape before Bedrock integration

### Current Verified Flow
```text
curl
↓
/plan
↓
app.py
↓
i2d2.process_intent()
↓
intent.extract_intent()
↓
Kre8Agent.extract_intent()   [stub]
↓
StructuredIntent
↓
Kre8Agent.call_llm()         [stub]
↓
Plan
↓
config validation
↓
JSON response
```

### To-Do
- Change the current curl-based interaction approach to a **UI-based** next
- Surface `StructuredIntent` more explicitly for debugging or intermediate visibility
- Begin replacing stubs incrementally
- Introduce `DesignPlan` after intent extraction stabilizes

### Next Step
- Decide the simplest first UI for the demo
- Keep current backend stable before introducing Bedrock integration


## Latest Updates (2026-03-21)

- Introduced kre8_realm, kre8_laws, kre8_arc
- Defined kiosk and whiteboard surfaces
- Adopted hybrid docs model (central + component READMEs)
- Finalized ARC naming (Architecture Catalog)
- Defined Structured Intent pause (Go / Review) flow
- Introduced single-repo multi-component structure with future lift-and-shift design
- Established separation between ideation and decisions (ADR-style decisions.md)
