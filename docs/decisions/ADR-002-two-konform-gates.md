# ADR-002: Two konform gates — kg1 (kit) and kg2 (kanvas)

**Status:** Active
**Date:** 2026-06-20

## Context

Policy enforcement could happen at any point in the pipeline. Options considered:

- **One gate post-kanvas only** — validate the final artifact before HCL synthesis.
  Simple, but expensive: a full kraph + kanvas assembly runs before discovering the
  intent was never permitted. Also loses early signal about why a design failed.

- **Inline validation per resource** — konform called per-resource during kraph
  generation. Fine-grained but couples the design loop tightly to policy evaluation,
  making retries complex and konform stateful.

- **Two gates: kg1 (post-kit) and kg2 (post-kanvas)** — policy checked at intent
  time and again at manifest time.

## Decision

Two explicit konform gates:

**kg1 — Kit gate** — runs after Kit extraction, before kraph generation. Validates
that the raw intent (resource types, regions, patterns) is permitted under the
active klue registry policies for this skope. A kg1 failure halts the pipeline
before any design work begins. Fast fail, cheap.

**kg2 — Kanvas gate** — runs after kanvas assembly, before koder. Validates the
full resolved manifest — explicit konfig values, resource configurations, cost
boundaries. kg2 catches what kg1 cannot: violations that only become visible once
vague intent is resolved into concrete values.

Both gates use the same klue registry policies. kg1 catches coarse violations;
kg2 catches boundary violations on resolved values.

## Consequences

- Design work only starts after kg1 passes — no wasted kraph generation on
  clearly impermissible intent
- kg2 failures are rare but meaningful — they indicate the resolved design
  exceeded a boundary that the raw intent did not
- konform is called twice per pipeline run with different artifact types
- kick (the resolved policy ID set) is produced before kg1 and used by both gates
