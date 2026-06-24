# ADR-004: i2d2 is sole design authority and sole katalog writer

**Status:** Active
**Date:** 2026-06-20

## Context

kre8's pipeline involves multiple components with visibility into design artifacts:
konform evaluates kanvas, koder consumes it, skout surfaces prior designs, skan
reads live infrastructure. Any of these could plausibly write to katalog or make
design adjustments in response to what they see.

Distributing write authority creates an audit problem: when an artifact in katalog
does not match what the pipeline produced, there is no single place to look. It
also creates a design authority problem: if konform can revise a kanvas to make it
compliant, or if koder can adjust a resource definition during synthesis, the
kanvas is no longer the single source of truth.

## Decision

i2d2 is the sole design authority and the sole writer to katalog across the entire
pipeline. Specifically:

- i2d2 extracts Kit and writes it to katalog
- i2d2 resolves kick and writes it to katalog
- i2d2 generates kraph and writes it to katalog
- i2d2 assembles kanvas and writes it to katalog
- i2d2 appends gate verdicts (from konform) to the kanvas record in katalog
- koder writes HCL to katalog — this is the one delegated write, scoped strictly
  to the HCL output artifact, under i2d2's invocation

No other component writes to katalog. konform returns a verdict to i2d2; i2d2
records it. skout returns findings to i2d2; i2d2 uses them in design. skan returns
live state to i2d2; i2d2 uses it as design context.

Design judgment — what resources to include, how to resolve vague intent, how to
structure dependencies — belongs exclusively to i2d2.

## Consequences

- katalog is always consistent with what i2d2 produced — no external writes to
  reconcile
- konform, skout, skan, and koder are all read-only or output-only from katalog's
  perspective
- Debugging any artifact in katalog means looking at i2d2's logic only
- Any future component that needs to "adjust" a design must do so by returning
  information to i2d2, not by writing to katalog directly
