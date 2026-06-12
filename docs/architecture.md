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
NLP → Kit → klue → kick → konform(kg1) → skout+skan → krux → knit(kwery) → kanvas → konform(kg2) → koder → HCL
```

### Stage Breakdown

| Stage | Component(s) | What happens |
|---|---|---|
| NLP → Kit | i2d2 + konnekt | Intent extracted into thin signal artifact. Values never normalized. |
| Kit → kick | klue | kick (Kit Inferred Contextual Klaws) produced — applicable policy IDs resolved from kit + skope. klue checks klues store in klaws before LLM inference. |
| Kit + kick → kg1 | konform | Kit validated against klaws. Pipeline halts on failure (unless kraken=true). |
| kg1 → skout + skan | skout, skan | Semantic search over kpedia + cloud infra scan for design aid. |
| skore + skan findings → krux | i2d2 + konnekt | Resource dependency graph generated. DAG + enum validated by Pydantic at construction time. Retry max 2, then design_conflicts[]. |
| krux → kanvas | knit + kwery | Provider konfig values resolved. Full infrastructure manifest assembled. |
| kanvas → kg2 | konform | Kanvas validated against klaws. Violations recorded in design_conflicts[]. |
| kanvas → HCL | koder + konnekt | HCL synthesized and written to katalog. |

---

## Key Data Contracts

| Artifact | Description |
|---|---|
| **Kit** | Thin. Intent signals extracted as-is from NLP. No normalization. |
| **kick** | Kit Inferred Contextual Klaws. Live per-run policy ID set produced by klue from kit + skope. |
| **klues** | The kick store inside klaws. Previously inferred kicks promoted for reuse. Not a pipeline artifact — owned by klaws, read by klue. |
| **krux** | Resource dependency graph — DAG of KruxResource nodes. |
| **kanvas** | Thick. Full infrastructure manifest — architecture decisions, resource map, konfig values, design conflicts. Single source of truth for koder. |
| **HCL** | Synthesized OpenTofu/Terraform-compatible code. |

Full schema definitions → `docs/schemas.md`

---

## Architecture Principles — Never Violate

1. **LLM is non-authoritative.** Structured JSON only — never directly generates or executes IaC.
2. **Kit is thin. Kanvas is thick.** Kit = intent signals. Kanvas = full infrastructure manifest.
3. **Policy gates are mandatory.** Kit and Kanvas must both pass konform/OPA before proceeding.
4. **Separation of concerns is strict.** Intent extraction, design reasoning, policy enforcement, HCL synthesis are isolated.
5. **No premature execution coupling.** Do not wire rendering or execution into design components.
6. **Flat-root repo structure.** No `packages/`, `apps/`, or nested monorepo wrappers.
7. **All LLM output must be Pydantic-validated.** No raw LLM strings passed downstream.
8. **MCP extractability is a first-class design constraint.** Clean, generic I/O contracts. No domain assumptions baked into interfaces. See ADR-010.
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
│   └── kure/            ← post-koder lint + self-correct (parked)
├── konform/             ← OPA policy engine wrapper (planned)
├── klaws/               ← Rego policy definitions + klues store (planned)
│   └── policies/
├── skope/               ← environment + workload skope (planned)
├── kiosk/               ← developer UI (planned)
├── konsole/             ← admin UI (planned)
├── katalog/             ← artifact store (planned)
├── klue/                ← kick inference engine (planned)
├── knit/                ← Kanvas assembler (planned)
├── kwery/               ← provider value resolver (planned)
├── skout/               ← semantic search + re-ranking (planned)
├── skan/                ← cloud infra scanner (parked)
├── kpedia/              ← RAG knowledge base (planned)
├── komb/                ← web scraper (planned)
├── gate/                ← API ingress (parked)
├── kron/                ← scheduler (planned)
├── kast/                ← Slack/webhook notifier (planned)
├── kli/                 ← CLI tool (parked)
├── stub_tests/          ← schema + stub validation
└── docs/
    ├── architecture.md  ← this file
    ├── components.md    ← component registry
    ├── schemas.md       ← schema reference
    ├── decisions/       ← ADR index + individual ADR files
    └── components/      ← per-component design specs
```
