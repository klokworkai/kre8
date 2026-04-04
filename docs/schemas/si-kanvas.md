# kre8 — Core Schema Definitions
**Last Updated:** April 2026

These are the two primary data contracts in the kre8 pipeline.
All LLM output must conform to these schemas via Pydantic v2 validation.

---

## Pipeline Position

```
NLP → [ StructuredIntent ] → konform → skout → [ Kanvas ] → konform → koder
```

---

## 1. StructuredIntent (SI)

**Thin schema.** Normalized high-level intent extracted from natural language.
Produced by kre8 (via konnekt/Clerk). Consumed by konform and then kre8 (Architect).

### Fields

| Field | Type | Description |
|---|---|---|
| `raw_input` | str | Original user NLP input |
| `goal` | str | Normalized summary of the infrastructure objective |
| `scope` | dict | Environment, team, platform hints |
| `signals` | dict | Extracted signals — regions, cloud provider, k8s, service mesh keywords |
| `constraints_hint` | dict | User-stated constraints — cost, security, region preferences |
| `realm_id` | str | Reference to active kontext realm |
| `questions` | list[str] | Blocking clarification questions before design can proceed |
| `confidence` | float | LLM confidence score (0.0–1.0) |
| `pause_for_review` | bool | If true, surface SI to user before proceeding to Kanvas |

### Philosophy
SI must be **provider-agnostic where possible**. It captures *what* the user wants, not *how* to build it. The *how* is Kanvas's job.

---

## 2. Kanvas (DP — Design Plan)

**Thick schema.** Full infrastructure manifest produced by kre8 (Architect reasoning).
Consumed by konform (policy validation) and then koder (HCL synthesis).

### Fields

| Field | Type | Description |
|---|---|---|
| `intent_summary` | str | Normalized summary of the user's request |
| `provider` | str | Target cloud provider (aws, gcp, azure) |
| `regions` | list[str] | Target deployment regions |
| `context` | dict | Infrastructure context — existing clusters, networks, accounts |
| `constraints_used` | dict | Applied kodex laws (LADE: Limit, Allow, Deny, Exception) |
| `design_options` | list[DesignOption] | Multiple viable architecture solutions |
| `recommended_option` | str | ID of the selected design option |
| `resources` | list[Resource] | High-level infrastructure components |
| `assumptions` | list[str] | Assumptions made when full information was unavailable |
| `questions` | list[str] | Clarifications needed before rendering or execution |
| `explanation` | str | Human-readable reasoning for the recommended design |
| `katalog_ref` | str \| None | Reference to matching katalog pattern if found by skout |

### LADE Policy Model (constraints_used)

| Code | Meaning |
|---|---|
| **L** — Limit | Constrain a resource (e.g. max instance size) |
| **A** — Allow | Explicitly permit a resource or pattern |
| **D** — Deny | Block a resource or pattern entirely |
| **E** — Exception | Override a Deny for a specific case |

### Philosophy
Kanvas is **not IaC**. It is a structured architecture decision that can be rendered into HCL by koder. It must be human-readable and auditable independently of the generated code.

---

## Schema Philosophy

```
Intent → StructuredIntent → Kanvas → HCL → Execute
```

- Each stage is independently validatable
- No stage can be skipped
- LLM output at each stage is Pydantic-validated before passing downstream
- Kanvas is the single source of truth for koder — koder never reads raw NLP
