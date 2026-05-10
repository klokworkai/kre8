# kre8 — System Architecture
**Product:** kre8 by klökwork AI
**Last Updated:** April 2026

---

## What kre8 Is

kre8 is a **Thinking Infrastructure Engine (TIE)**. It translates natural language infrastructure intent into validated, policy-aware design plans and executable HCL.

kre8 is not an IaC generator. It is a **decision engine** — it produces structured, traceable, policy-governed design artifacts before any code is synthesized.

`i2d2` (Intelligent Infrastructure Design Decision) is the reasoning engine inside kre8. `kre8` is the what. `i2d2` is the how. `i2d2.py` is the orchestration entry point.

---

## Competitive Position

| Product | Approach | Gap |
|---|---|---|
| StackGen / Aiden | NL → module catalog → Terraform | No explicit design artifact. Black box. |
| Spacelift Intent | NL → cloud APIs directly | No HCL. Prototyping only. |
| **kre8** | NL → Kit → Kanvas → HCL | i2d2 surfaces design as an explicit, inspectable, policy-validated artifact (Kanvas) before synthesis. **Design transparency is the moat.** |

---

## Full Pipeline

```
NLP → Kit → klue → kick → konform(kg1) → skout+skan → krux → knit(kwery) → kanvas → konform(kg2) → koder → HCL
```

### Stage Breakdown

| Stage | Component(s) | What happens |
|---|---|---|
| NLP → Kit | i2d2 + konnekt (Clerk) | Intent extracted into thin signal artifact. Values never normalized. |
| Kit → kick | klue | kick (Kit Inferred Contextual Klaws) produced — applicable policy IDs resolved from kit + kontext. klue checks klues store in klaws before LLM inference. |
| Kit + kick → kg1 | konform | Kit validated against klaws. Pipeline halts on failure (unless kraken=true). |
| kg1 → skout + skan | skout, skan | Semantic search over kpedia + cloud infra scan for design aid. skout produces skore. |
| skore + skan findings → krux | i2d2 + konnekt (Architect) | Resource dependency graph generated. DAG + enum validated by Pydantic at construction time. Retry max 2, then design_conflicts[]. |
| krux → kanvas | knit + kwery | Provider konfig values resolved. Full infrastructure manifest assembled. |
| kanvas → kg2 | konform | Kanvas validated against klaws. Violations recorded in design_conflicts[]. |
| kanvas → HCL | koder + konnekt (Coder) | HCL synthesized and written to katalog. |

---

## Key Data Contracts

| Artifact | Description |
|---|---|
| **Kit** | Thin. Intent signals extracted as-is from NLP. No normalization. |
| **kick** | Kit Inferred Contextual Klaws. Live per-run policy ID set produced by klue from kit + kontext. |
| **klues** | The kick store inside klaws. Previously inferred kicks promoted for reuse. Not a pipeline artifact — owned by klaws, read by klue. |
| **krux** | Resource dependency graph — DAG of KruxResource nodes. |
| **skore** | skout's re-ranked search results. Produced by skout, stored in kpedia, passed to i2d2 pre-Kanvas. |
| **Kanvas** | Thick. Full infrastructure manifest — architecture decisions, resource map, konfig values, design conflicts. Single source of truth for koder. |
| **HCL** | Synthesized OpenTofu/Terraform-compatible code. |

Full schema definitions → `klokwork-design-log/kre8/schemas.md`

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
9. **Kit never normalizes.** Extracted signal values are as-is from NLP. Resolution is a kontext-informed i2d2 concern during Kanvas design.
10. **DAG validation is i2d2's responsibility.** Pydantic model validator on krux at construction time. i2d2 retry loop max 2, beyond that → design_conflicts[]. konform does not own structural validation.

---

## Phase 1 MVP Pipeline

The Phase 1 pipeline is stubbed end-to-end with real I/O contracts. Only the critical path is real — everything else is stubbed in-memory.

```
kiosk       (real — input box + submit + HCL output display)
  → i2d2    (real — orchestration + Kit extraction + Krux generation)
    → konnekt   (real — LLM adapter)
    → katalog   (stub — in-memory)
  → koder   (real — HCL synthesis)
```

---

## Model Routing (via konnekt)

| Task | Role | Model |
|---|---|---|
| Intent extraction | Clerk | GPT-4o-mini |
| Design reasoning | Architect | Claude Sonnet (Opus for High/Critical — threshold TBD) |
| HCL synthesis | Coder | DeepSeek-V3 |
| Self-correction | Medic | Groq Llama 3.3 |

Model names live in `konnekt/` only. Opus toggle logic lives in `i2d2/` only.

---

## Versioning Model

| Segment | Increment when |
|---|---|
| `v0 → v1` | Full pipeline real, no stubs in critical path, external users onboarded |
| `x.N.0` | New component goes stub → real, or new component added to pipeline |
| `x.x.N` | Schema field added/changed, prompt tuning, bug fix, stub behaviour changed |

| Phase | Version range | Exit gate |
|---|---|---|
| Phase 1 MVP | v0.1.0 | End-to-end: NLP → Kit → Kanvas → HCL. kiosk + i2d2 + konnekt + koder real. katalog stubbed. |
| Phase 2.1 | v0.2.0 – v0.3.0 | Policy gates + semantic search real |
| Phase 2.2 | v0.4.0 | Post-gen validation + self-correction real |
| Phase 3 | v1.0.0 | Ship-ready — auth, konsole, no stubs in critical path |

---

## Repository Structure

```
klokworkai/kre8          ← mono-repo
├── i2d2/                ← reasoning engine + orchestrator
├── konnekt/             ← LLM adapter
├── koder/               ← HCL synthesizer
│   └── kure/            ← post-koder lint + self-correct (parked)
├── konform/             ← OPA policy engine wrapper
├── klaws/               ← Rego policy definitions + klues store
│   └── policies/
├── kontext/             ← environment + workload context
├── kiosk/               ← developer UI
├── konsole/             ← admin UI (Phase 3)
├── katalog/             ← artifact store (Phase 2.1)
├── klue/                ← kick inference engine (Phase 2.1)
├── knit/                ← Kanvas assembler (Phase 2.1)
├── kwery/               ← provider value resolver (Phase 2.1)
├── skout/               ← semantic search + re-ranking (Phase 2.1)
│   └── skore/           ← re-ranked results artifact (parked)
├── skan/                ← cloud infra scanner (in progress)
├── kpedia/              ← RAG knowledge base (Phase 2.1)
├── komb/                ← web scraper (Phase 2.1)
├── gate/                ← API ingress (parked)
├── kron/                ← scheduler (Phase 2.2)
├── kast/                ← Slack/webhook notifier (Phase 3)
├── stub_tests/          ← schema + stub validation
└── docs/
```

Design log, ADRs, and component specs → `klokworkai/klokwork-design-log`
