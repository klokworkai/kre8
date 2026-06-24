# ADR-001: LLM is non-authoritative — structured JSON only, Pydantic-validated, never executes IaC

**Status:** Active
**Date:** 2026-06-20

## Context

kre8 uses LLMs as reasoning engines at multiple pipeline stages — Kit extraction,
kick resolution, kraph generation, and HCL synthesis. The temptation at every stage
is to trust the LLM output directly: pass the raw string downstream, let the model
write HCL directly, or treat a well-formed response as correct by inspection.

LLMs hallucinate. They produce plausible-looking but structurally invalid output.
They cannot be audited. And in an infrastructure context, a confident but wrong
output that reaches a provider API causes real damage.

## Decision

LLM output is never authoritative. Every LLM response in the kre8 pipeline must:

1. Be requested as structured JSON (via prompt instruction and/or response format)
2. Be validated immediately against a Pydantic model before any downstream use
3. Never directly generate or execute IaC — koder synthesizes HCL from a
   validated kanvas artifact, not from free-form LLM output

Raw LLM strings never cross a component boundary. If validation fails, the caller
handles the failure — retry, conflict recording, or surface to user. The LLM never
decides what happens next.

## Consequences

- Every pipeline stage that calls konnekt owns the Pydantic validation of the response
- koder receives a validated kanvas, not a prompt — it synthesizes HCL deterministically from that contract
- Prompt engineering is always in service of structured output, never narrative output
- Adding a new LLM call to the pipeline requires a corresponding Pydantic model
