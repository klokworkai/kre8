# ADR-003: konform is purely stateless — verdict only, never writes, never designs

**Status:** Active
**Date:** 2026-06-20

## Context

konform sits at two critical points in the pipeline and has visibility into both
the raw intent (kit) and the full infrastructure manifest (kanvas). That makes it
a tempting place to add behaviour: cache verdicts, suggest policy-compliant
alternatives, write audit records, or nudge the design toward compliance.

Every one of those additions would compromise its reliability as a judge.

## Decision

konform is a pure stateless judge. Its contract is:

- **Input:** artifact (kit or kanvas) + kick (resolved policy ID set)
- **Output:** `{ pass: bool, violated_policy_ids: [str] }`
- **Side effects:** none

konform never writes to katalog or any persistent store. It never produces a
design, suggests an alternative, or revises an artifact. It never reads prior
verdicts to inform the current one. Each gate call is fully self-contained.

Structural validation (DAG correctness, schema conformance) is not konform's
responsibility — that belongs to i2d2 via Pydantic. konform evaluates policy
only: is this artifact permitted under the active klue registry rules?

## Consequences

- konform can be called, tested, and reasoned about in complete isolation
- Audit logging, if added, is i2d2's responsibility — i2d2 writes the verdict
  to katalog alongside the artifact, not konform
- konform is a strong MCP candidate precisely because of this contract — a
  stateless judge with clean I/O can be extracted and run by any consumer
- Any future request to "have konform suggest fixes" is explicitly out of scope
