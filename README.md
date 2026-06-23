# kre8 — Intent to Infra

> ⚠️ **Work in Progress** — kre8 is under active development. The pipeline architecture is being actively simplified and most components are not yet implemented. Not ready for production use.

---

## What is kre8?

**kre8** is a **Thinking Infrastructure Engine (TIE)** — it translates natural language infrastructure intent into validated, policy-aware design decisions and executable HCL.

At its core is **i2d2** (Intelligent Infrastructure Design Decision) — the reasoning engine that transforms raw intent into a structured, inspectable design artifact (Kanvas) before any code is synthesized. Design transparency is the differentiator: kre8 shows its work before it writes a single line of HCL.

---

## How it works

```
NLP → Kit → kick → konform(kg1) → kraph → kanvas → konform(kg2) → koder → HCL
```

1. **Kit** — extracts intent signals from natural language (never normalized); stored as its own artifact, reusable across environments
2. **kick + konform(kg1)** — i2d2 resolves applicable policies from the klue registry, validates intent before design begins
3. **i2d2** — reasons over kit + kick (consulting prior designs and live infra scans as needed) to produce a resource dependency graph (kraph)
4. **i2d2** — resolves provider config values and assembles the full infrastructure manifest (kanvas)
5. **konform(kg2)** — validates the full design against policies before any code is written
6. **koder** — synthesizes HCL from the validated kanvas, strictly implementing what kanvas specifies

---

## Current State

| Component | Status | Notes |
|---|---|---|
| konnekt | ✅ Done | Full LLM adapter — 5 provider families, GCP SM secrets |
| Kit schema | ✅ Done | 14 signal categories, standalone artifact with its own ID, in `i2d2/schemas.py` |
| Kraph schema | ✅ Done | DAG validation, layer model, depends_on, Mermaid DSL field — implemented in `i2d2/schemas.py` |
| Kanvas schema | ✅ Done | Gate verdicts, design_conflicts — implemented in `i2d2/schemas.py` |
| i2d2 | 🔄 In progress | FastAPI live, Kit extraction wired — now also owns kick resolution and kanvas assembly directly; koder not yet called |
| kiosk | ⬜ Planned | Developer UI |
| koder | ⬜ Planned | HCL synthesizer |
| katalog | ⬜ Planned | Artifact store (stub first) |
| konform, klue registry, skope, skout, skan, kpedia | ⬜ Planned | Post-MVP |

---

## Documentation

*docs/ is being updated to match the simplified pipeline above.*

- [Architecture](docs/architecture.md) — pipeline, principles, build state
- [Components](docs/components.md) — full component registry
- [Schemas](docs/schemas.md) — Kit, Kraph, Kanvas schema reference
- [ADRs](docs/decisions/README.md) — architecture decision index

---

## Tech Stack

- Python 3.11+ · Pydantic v2 · FastAPI
- LLM routing via [LiteLLM](https://github.com/BerriAI/litellm) (konnekt)
- Policy enforcement via [OPA](https://www.openpolicyagent.org/) + Rego (konform/klue registry — planned)
- HCL output: OpenTofu/Terraform-compatible

---

**GitHub:** [klokworkai/kre8](https://github.com/klokworkai/kre8)

![kre8 Logo](./kre8-logo.png)
