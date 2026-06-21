# ADR-005: DAG validation is owned by i2d2, not konform

**Status:** Active
**Date:** 2026-06-20

## Context

krux is a resource dependency graph (DAG). Validating that graph — checking for
cycles, confirming depends_on references resolve, enforcing that app-layer resources
only depend on foundation-layer resources — is a structural concern.

konform is the policy gate. The natural assumption is that konform owns all
validation. That assumption is wrong here, and getting it wrong has consequences:
konform is stateless and policy-scoped; structural graph validation is neither.

## Decision

DAG validation and all structural krux validation is owned by i2d2, implemented
as Pydantic model validators on the Krux schema. It runs at construction time —
the moment i2d2 assembles the krux from LLM output.

Validation rules enforced by i2d2:

- Every resource has a non-empty `layer` list with values in `{foundation, app, data}`
- Every `type` matches `<namespace>:<resource_type>` format
- Every `depends_on[].ref` resolves to a local resource id or a declared `$inputs.<name>`
- Every local `depends_on` target has `foundation` in its layer
- The `(role, ref)` pair is type-consistent
- The dependency graph is acyclic
- No two resources share an id
- Required inputs are supplied

On validation failure: i2d2 retries LLM krux generation up to 2 times. Beyond
that, failures are recorded in `design_conflicts[]` and the pipeline surfaces them
to the user rather than halting silently.

konform is never called for structural issues. konform evaluates policy only.

## Consequences

- Structural failures are caught before konform is ever called — no wasted gate
  evaluation on a malformed graph
- The retry loop lives in i2d2, which is the only component with the context to
  regenerate a krux
- konform's contract stays clean — it evaluates policy, not structure
- Adding a new structural rule means adding a Pydantic validator to Krux, not
  modifying konform
