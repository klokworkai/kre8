# ADR-007: Kit never normalizes — signal values extracted as-is

**Status:** Active
**Date:** 2026-06-20

## Context

During Kit extraction, i2d2 pulls intent signals from raw NLP input. The temptation
is to normalize at extraction time: convert "super fast" to a latency value, resolve
"cheap" to a cost tier, map "postgres" to a canonical resource type. It feels
helpful — the downstream design step gets clean, typed values instead of freeform
strings.

Normalization at extraction time is the wrong place. It collapses signal
information before the context needed to resolve it correctly is available. "Cheap"
means different things under different skopes. "Postgres" might map to different
managed services depending on region, environment, and policy. Normalizing early
produces false precision — a specific value where the intent was genuinely vague.

## Decision

Kit extraction is a read operation, not a resolve operation. Signal values are
extracted exactly as they appear in the NLP input — no normalization, no mapping,
no inference beyond identifying that a signal is present and which category it
belongs to.

Resolution happens in i2d2 during krux generation, informed by skope and the
active klue registry policies (via kick). At that point, the full context is
available: what the skope permits, what policies constrain, what prior designs
suggest.

The `inferred: bool` field on each signal captures whether i2d2 inferred the
signal's presence (it was implied but not stated). Signal values are never
modified — only their presence is inferred.

## Consequences

- Kit is a faithful representation of what the user said, not what the system
  thinks they meant
- The same Kit can be re-resolved under a different skope and produce a different
  design — cross-skope reuse is valid because Kit carries raw intent, not resolved
  decisions
- Downstream components (krux generation, konform) receive vague values and must
  handle them — this is intentional
- Debugging a design decision traces back to i2d2's resolution logic, not Kit
  extraction — Kit is always inspectable as a clean record of original intent
