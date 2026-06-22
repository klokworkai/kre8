# kre8 — System Architecture
**Last Updated:** June 2026

---

## What kre8 Is

kre8 is a **Thinking Infrastructure Engine (TIE)**. It translates natural language infrastructure intent into validated, policy-aware design plans and executable HCL.

kre8 is not an IaC generator. It is a **decision engine** — it produces structured, traceable, policy-governed design artifacts before any code is synthesized.

`i2d2` (Intelligent Infrastructure Design Decision) is the reasoning engine inside kre8. `kre8` is the what. `i2d2` is the how. `i2d2.py` is the orchestration entry point.

---

## Full Pipeline

```
NLP → Kit → kick → konform(kg1) → krux → kanvas → konform(kg2) → koder → HCL
```

> skout and skan are summoned by i2d2 during krux generation as needed — not pipeline stages.

### Stage Breakdown

| Stage | Component(s) | What happens |
|---|---|---|
| NLP → Kit | i2d2 + konnekt | Intent extracted into thin signal artifact. Values never normalized. |
| Kit → kick | i2d2 | kick produced — kit_id + resolved klue registry policy IDs. i2d2 reads klue registry directly and infers via its own LLM call. Checks katalog for existing matching kick before re-resolving. |
| Kit + kick → kg1 | konform | Kit + kick validated against klue registry. Pipeline halts on failure (unless kraken=true). |
| kg1 → krux | i2d2 + konnekt | skout and skan optionally summoned for design context. Resource dependency graph generated. DAG validated by Pydantic at construction time. Retry max 2, then design_conflicts[]. Trail of skout/skan findings recorded in krux.references. |
| krux → kanvas | i2d2 + konnekt | Config values resolved. Full infrastructure manifest assembled directly by i2d2. |
| kanvas → kg2 | konform | Kanvas validated against klue registry. Violations recorded in design_conflicts[]. Kanvas always stored in katalog regardless of kg2 outcome. |
| kanvas → HCL | koder + konnekt | HCL synthesized and written to katalog. |

---

## Key Data Contracts

| Artifact | Description |
|---|---|
| **Kit** | Thin. Intent signals extracted as-is from NLP. No normalization. Standalone artifact — reusable across skopes. |
| **kick** | kit_id + resolved klue registry policy IDs for this run. Produced by i2d2. |
| **krux** | Resource dependency graph — DAG of KruxResource nodes. Carries references trail of skout/skan findings. |
| **kanvas** | Thick. Full infrastructure manifest — architecture decisions, resource map, konfig values, design conflicts. Single source of truth for koder. Always stored in katalog regardless of kg2 outcome. |
| **HCL** | Synthesized OpenTofu/Terraform-compatible code. |

Full schema definitions → `docs/schemas.md`

---

## Architecture Principles — Never Violate

1. **LLM is non-authoritative.** Structured JSON only — never directly generates or executes IaC.
2. **Kit is thin. Kanvas is thick.** Kit = intent signals. Kanvas = full infrastructure manifest.
3. **Policy gates are mandatory.** Kit and Kanvas must both pass konform/OPA before proceeding.
4. **Policy judgment is the one strictly isolated concern.** konform never writes to katalog and never produces or revises a design. i2d2 is the sole design authority and sole katalog writer across intent extraction, kick resolution, krux generation, and kanvas assembly.
5. **No premature execution coupling.** Do not wire rendering or execution into design components.
6. **Flat-root repo structure.** No `packages/`, `apps/`, or nested monorepo wrappers.
7. **All LLM output must be Pydantic-validated.** No raw LLM strings passed downstream.
8. **Clean, generic I/O contracts.** No domain assumptions baked into interfaces.
9. **Kit never normalizes.** Extracted signal values are as-is from NLP. Resolution is a skope-informed i2d2 concern during Kanvas design.
10. **DAG validation is i2d2's responsibility.** Pydantic model validator on krux at construction time. i2d2 retry loop max 2, beyond that → design_conflicts[]. konform does not own structural validation.

---

## Current Build State (Phase 1 MVP)

Only the critical path is being built first — everything else is not started or parked.

```
kiosk       (TODO)
  → i2d2    (INPROGRESS — FastAPI live, Kit extraction wired, koder not yet called)
    → konnekt   (DONE — full LLM adapter)
    → katalog   (TODO — stub in-memory)
  → koder   (TODO)
```

---

## Repository Structure

```
klokworkai/kre8
├── i2d2/                ← reasoning engine + orchestrator
├── konnekt/             ← LLM adapter
├── koder/               ← HCL synthesizer (planned)
│   └── kure/            ← post-koder lint + self-correct (deferred)
├── konform/             ← OPA policy engine wrapper (not started)
├── klue_registry/       ← policy definitions — pure data store (not started)
├── skope/               ← environment + workload skope (not started)
├── kiosk/               ← developer UI (planned)
├── konsole/             ← admin UI (not started)
├── katalog/             ← artifact store (planned)
├── skout/               ← semantic search + re-ranking (not started)
├── skan/                ← cloud infra scanner (not started)
├── kpedia/              ← RAG knowledge base (not started)
├── kast/                ← Slack/webhook notifier (not started)
├── stub_tests/          ← schema + stub validation
└── docs/
    ├── architecture.md  ← this file
    ├── components.md    ← component registry
    ├── schemas.md       ← schema reference
    ├── decisions/       ← ADR index + individual ADR files
    └── components/      ← per-component design specs
```
