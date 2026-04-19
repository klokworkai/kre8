# kre8 — Intent to Infra

![kre8 Logo](./kre8-logo.png)

---
# kre8 by klökwork AI

**kre8** is a **Thinking Infra Engine (TIE)** — context-aware, thinks, designs, and builds cloud infrastructure from natural language intent.

At its core is **i2d2** (Intelligent Infrastructure Design Decision) — the reasoning engine that transforms raw intent into structured, policy-validated infrastructure design decisions before any HCL is generated and emboies true **Intent to Infra**.

---

## Core Pipeline

```
NLP Input
  → kre8  (intent extraction → StructuredIntent)
  → konform  (SI validated against kodex policies)
  → skout  (semantic search: katalog + kpedia)
  → kloud-skan  (reads current infra state)
  → kre8  (Kanvas design reasoning)
  → konform  (Kanvas validated against kodex)
  → koder  (HCL synthesis via Context7)
  → kure  (validate + self-correct)
  → kiosk  (HCL + Mermaid blueprint → developer)
```

---

## Components

See [docs/components.md](docs/components.md) for the full phased component registry.

| Component | Folder | Phase | Role |
|---|---|---|---|
| kre8 | `kre8/` | 1 | Brain — i2d2 orchestrator, NLP→SI→Kanvas |
| konnekt | `konnekt/` | 1 | LLM adapter/agent router (LiteLLM) |
| koder | `koder/` | 1 | HCL synthesis (DeepSeek-V3 + Context7) |
| kure | `koder/kure/` | 1 | Validate + self-correct (Checkov + OpenTofu) |
| konform | `konform/` | 1 | OPA policy engine wrapper |
| kodex | `kodex/` | 1 | Rego policy definitions (LADE model) |
| kontext | `kontext/` | 1 | Environment/workload context |
| kiosk | `kiosk/` | 1 | Developer UI — prompt in, HCL out |
| konsole | `konsole/` | 1 | Admin UI — kontext, kodex, konnekt config |

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for principles and pipeline detail.

**GitHub:** [klokworkai/kre8](https://github.com/klokworkai/kre8)
**Mono-repo** — components will be split into individual repos in a future phase.

---

## Current State

- End-to-end pipeline wired with stub logic
- `StructuredIntent` schema in `kre8/intent_models.py` — basic, full schema is next milestone
- `Kanvas` specced in `docs/schemas/si-kanvas.md` — not yet implemented as Pydantic model
- No real LLM integration yet
- No OPA integration yet
- No HCL synthesis yet

**Next milestone:** Full SI Pydantic schema → Kanvas schema → real LLM calls via konnekt
