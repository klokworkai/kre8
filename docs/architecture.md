# kre8 — System Architecture
**Product:** kre8 by klökwork AI
**Last Updated:** April 2026

---

## What kre8 Is

kre8 is a Thinking Infra Engine (TIE). It translates natural language infrastructure intent into validated, policy-aware design plans and executable HCL code.

kre8 is **not** just an IaC generator. It is a **decision engine** that produces structured, traceable, policy-governed outputs.

The `i2d2` component is the engine — it owns the full orchestration logic from NLP to Kanvas to Iac.

---

## Core Pipeline

```
NLP Input
  → kre8 (intent extraction via konnekt/Clerk → kit)
  → konform (kit validated against kodex)
  → skout (search katalog + kpedia for matching patterns)
  → kre8 (kanvas reasoning via konnekt/Architect)
  → konform (kanvas validated against kodex)
  → koder (HCL synthesis via Context7, utd_docs + konnekt/Coder)
  → kure (validate + self-correct loop) 
  → kiosk ((deliver: HCL + Mermaid blueprint + artifacts rendered to developer)
```

---

## Key Data Contracts

| Schema | Description |
|---|---|
| **kit** | Thin — normalized high-level intent extracted from NLP |
| **kanvas** | Thick — full infrastructure manifest, architecture decisions, resource map |

See `docs/schemas/si-kanvas.md` for full spec.

---

## Architectural Principles

1. **LLM is non-authoritative.** LLM produces structured JSON only. Never directly generates or executes IaC.
2. **kit is thin. kanvas is thick.** kit = high-level normalized intent. kanvas = full infrastructure manifest.
3. **Policy gates are mandatory.** kit and kanvas must both pass OPA/konform validation before proceeding.
4. **Separation of concerns is strict.** Intent extraction, design reasoning, policy enforcement, and HCL synthesis are isolated.
5. **No premature execution coupling.** Rendering and execution are never wired into design components.
6. **Flat-root repo structure.** No nested monorepo wrappers. All components at repo root.
7. **All LLM output is Pydantic-validated.** No raw LLM strings passed downstream.

---

## Component Overview

See `docs/components.md` for the full phased component registry.

### Phase 1 (Pilot) — Active
```
kiosk → kre8 → konnekt → konform/kodex → koder → kure → kiosk
                ↕
             kontext
```

### Phase 2+ (Planned)
Adds: skout, katalog, kpedia, komb, kron, gate, konsole, kast, kick
